# Add this to app/routes/__init__.py
from flask import Blueprint, jsonify
from app.utils.cache import get_low_stock_alerts
from app.models.product import Product

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
def list_alerts():
    # Get product IDs with low stock
    low_stock_product_ids = get_low_stock_alerts()
    
    # Get product details
    low_stock_products = Product.query.filter(Product.id.in_(low_stock_product_ids)).all()
    
    result = [{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'min_stock_level': p.min_stock_level,
        'warehouse_id': p.warehouse_id,
        'warehouse_name': p.warehouse.name
    } for p in low_stock_products]
    
    return jsonify(result)