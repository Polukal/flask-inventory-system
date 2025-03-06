from flask import Blueprint, request, jsonify
from app import db
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.utils.cache import (
    get_stock_level, set_stock_level, 
    cache_warehouse, get_cached_warehouse,
    get_low_stock_alerts
)
from app.utils.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

warehouse_bp = Blueprint('warehouses', __name__)

@warehouse_bp.route('/', methods=['POST'])
def add_warehouse():
    data = request.json
    warehouse = Warehouse(
        name=data['name'],
        location=data['location']
    )
    db.session.add(warehouse)
    db.session.commit()
    
    # Cache warehouse
    cache_warehouse(warehouse)
    
    return jsonify({
        'message': 'Warehouse added successfully',
        'warehouse': warehouse.to_dict()
    }), 201

@warehouse_bp.route('/', methods=['GET'])
def list_warehouses():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    limit = min(
        int(request.args.get('limit', DEFAULT_PAGE_SIZE)), 
        MAX_PAGE_SIZE
    )
    offset = (page - 1) * limit
    
    # Get total count for pagination metadata
    total_count = Warehouse.query.count()
    
    # Get paginated warehouses
    warehouses = Warehouse.query.offset(offset).limit(limit).all()
    
    result = {
        'items': [w.to_dict() for w in warehouses],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total_count,
            'pages': (total_count + limit - 1) // limit
        }
    }
    
    return jsonify(result)

@warehouse_bp.route('/<int:warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    # Try to get from cache first
    cached_warehouse = get_cached_warehouse(warehouse_id)
    if cached_warehouse:
        return jsonify(cached_warehouse)
    
    # If not in cache, get from database
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    # Cache for future requests
    cache_warehouse(warehouse)
    
    return jsonify(warehouse.to_dict())

@warehouse_bp.route('/<int:warehouse_id>/products', methods=['GET'])
def list_warehouse_products(warehouse_id):
    # Ensure warehouse exists
    Warehouse.query.get_or_404(warehouse_id)
    
    # Pagination parameters
    page = int(request.args.get('page', 1))
    limit = min(
        int(request.args.get('limit', DEFAULT_PAGE_SIZE)), 
        MAX_PAGE_SIZE
    )
    offset = (page - 1) * limit
    
    # Get total count for pagination metadata
    total_count = Product.query.filter_by(warehouse_id=warehouse_id).count()
    
    # Get paginated products
    products = Product.query.filter_by(warehouse_id=warehouse_id)\
                            .offset(offset).limit(limit).all()
    
    result = {
        'items': [p.to_dict() for p in products],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total_count,
            'pages': (total_count + limit - 1) // limit
        }
    }
    
    return jsonify(result)

@warehouse_bp.route('/transfer', methods=['POST'])
def transfer_products():
    data = request.json
    
    product_id = data['product_id']
    source_warehouse_id = data['source_warehouse_id']
    destination_warehouse_id = data['destination_warehouse_id']
    quantity = data['quantity']
    
    # Validate source warehouse has the product
    product = Product.query.filter_by(
        id=product_id, 
        warehouse_id=source_warehouse_id
    ).first_or_404("Product not found in source warehouse")
    
    # Check if destination warehouse exists
    Warehouse.query.get_or_404(destination_warehouse_id)
    
    # Check current stock level
    current_stock = get_stock_level(product_id)
    
    if current_stock is None:
        # Calculate from database if not in cache
        additions = db.session.query(db.func.sum(StockMovement.quantity)).filter(
            StockMovement.product_id == product_id,
            StockMovement.destination_warehouse_id == source_warehouse_id
        ).scalar() or 0
        
        removals = db.session.query(db.func.sum(StockMovement.quantity)).filter(
            StockMovement.product_id == product_id,
            StockMovement.source_warehouse_id == source_warehouse_id
        ).scalar() or 0
        
        current_stock = additions - removals
        
    # Ensure there's enough stock
    if current_stock < quantity:
        return jsonify({
            'error': 'Insufficient stock',
            'available': current_stock,
            'requested': quantity
        }), 400
    
    # Create transfer movement
    movement = StockMovement(
        product_id=product_id,
        source_warehouse_id=source_warehouse_id,
        destination_warehouse_id=destination_warehouse_id,
        quantity=quantity,
        movement_type='transfer'
    )
    
    # Update product warehouse
    product.warehouse_id = destination_warehouse_id
    
    db.session.add(movement)
    db.session.commit()
    
    # Update cache
    # Reduce stock at source
    set_stock_level(product_id, current_stock - quantity, product.min_stock_level)
    
    return jsonify({
        'message': 'Product transferred successfully',
        'movement': {
            'id': movement.id,
            'product_id': movement.product_id,
            'source_warehouse_id': movement.source_warehouse_id,
            'destination_warehouse_id': movement.destination_warehouse_id,
            'quantity': movement.quantity,
            'timestamp': movement.timestamp.isoformat()
        }
    })