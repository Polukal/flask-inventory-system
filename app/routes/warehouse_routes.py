from flask import Blueprint, request, jsonify
from app import db
from app.models.warehouse import Warehouse

warehouse_bp = Blueprint('warehouses', __name__)

@warehouse_bp.route('/', methods=['POST'])
def add_warehouse():
    data = request.json
    warehouse = Warehouse(name=data['name'], location=data['location'])
    db.session.add(warehouse)
    db.session.commit()
    return jsonify({'message': 'Warehouse added successfully'}), 201

@warehouse_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Inventory Management API!"})