from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.utils.cache import (
    get_stock_level, set_stock_level, 
    cache_product, get_cached_product
)
from app.utils.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.json
    product = Product(
        name=data['name'],
        description=data.get('description'),
        sku=data.get('sku'),
        min_stock_level=data.get('min_stock_level', 10),
        warehouse_id=data['warehouse_id']
    )
    
    db.session.add(product)
    db.session.commit()
    
    # Add initial stock movement if stock value provided
    if 'stock' in data and data['stock'] > 0:
        movement = StockMovement(
            product_id=product.id,
            destination_warehouse_id=product.warehouse_id,
            quantity=data['stock'],
            movement_type='addition'
        )
        db.session.add(movement)
        db.session.commit()
        
        # Cache the stock level
        set_stock_level(product.id, data['stock'], product.min_stock_level)
    
    # Cache product details
    cache_product(product)
    
    return jsonify({
        'message': 'Product added successfully',
        'product': product.to_dict()
    }), 201

@product_bp.route('/', methods=['GET'])
def list_products():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    limit = min(
        int(request.args.get('limit', DEFAULT_PAGE_SIZE)), 
        MAX_PAGE_SIZE
    )
    offset = (page - 1) * limit
    
    warehouse_id = request.args.get('warehouse_id')
    
    # Query builder
    query = Product.query
    
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)
    
    # Get total count for pagination metadata
    total_count = query.count()
    
    # Get paginated products
    products = query.offset(offset).limit(limit).all()
    
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

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Try to get from cache first
    cached_product = get_cached_product(product_id)
    if cached_product:
        return jsonify(cached_product)
    
    # If not in cache, get from database
    product = Product.query.get_or_404(product_id)
    
    # Cache for future requests
    cache_product(product)
    
    return jsonify(product.to_dict())

@product_bp.route('/<int:product_id>/stock', methods=['GET'])
def get_product_stock(product_id):
    # Try to get from cache first
    stock = get_stock_level(product_id)
    
    # If not in cache, calculate from database
    if stock is None:
        # Calculate stock based on movements
        additions = db.session.query(db.func.sum(StockMovement.quantity)).filter(
            StockMovement.product_id == product_id,
            StockMovement.destination_warehouse_id.isnot(None)
        ).scalar() or 0
        
        removals = db.session.query(db.func.sum(StockMovement.quantity)).filter(
            StockMovement.product_id == product_id,
            StockMovement.source_warehouse_id.isnot(None)
        ).scalar() or 0
        
        stock = additions - removals
        
        # Cache the calculated value
        product = Product.query.get_or_404(product_id)
        set_stock_level(product_id, stock, product.min_stock_level)
    
    return jsonify({
        'product_id': product_id,
        'stock_level': stock
    })

@product_bp.route('/<int:product_id>/movements', methods=['GET'])
def get_product_movements(product_id):
    # Ensure product exists
    Product.query.get_or_404(product_id)
    
    # Pagination parameters
    page = int(request.args.get('page', 1))
    limit = min(
        int(request.args.get('limit', DEFAULT_PAGE_SIZE)), 
        MAX_PAGE_SIZE
    )
    offset = (page - 1) * limit
    
    # Query movements
    movements = StockMovement.query.filter_by(product_id=product_id)\
                                    .order_by(StockMovement.timestamp.desc())\
                                    .offset(offset).limit(limit).all()
    
    # Get total count for pagination metadata
    total_count = StockMovement.query.filter_by(product_id=product_id).count()
    
    result = {
        'items': [{
            'id': m.id,
            'movement_type': m.movement_type,
            'quantity': m.quantity,
            'source_warehouse_id': m.source_warehouse_id,
            'source_warehouse_name': m.source_warehouse.name if m.source_warehouse else None,
            'destination_warehouse_id': m.destination_warehouse_id,
            'destination_warehouse_name': m.destination_warehouse.name if m.destination_warehouse else None,
            'timestamp': m.timestamp.isoformat()
        } for m in movements],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total_count,
            'pages': (total_count + limit - 1) // limit
        }
    }
    
    return jsonify(result)