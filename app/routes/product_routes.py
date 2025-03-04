from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.json
    product = Product(name=data['name'], stock=data['stock'], warehouse_id=data['warehouse_id'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201

@product_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Inventory Management API!"})