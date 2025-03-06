from app import db
from datetime import datetime

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    source_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=True)
    destination_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)  # 'addition', 'removal', 'transfer'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    source_warehouse = db.relationship('Warehouse', foreign_keys=[source_warehouse_id])
    destination_warehouse = db.relationship('Warehouse', foreign_keys=[destination_warehouse_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'source_warehouse_id': self.source_warehouse_id,
            'source_warehouse_name': self.source_warehouse.name if self.source_warehouse else None,
            'destination_warehouse_id': self.destination_warehouse_id,
            'destination_warehouse_name': self.destination_warehouse.name if self.destination_warehouse else None,
            'quantity': self.quantity,
            'movement_type': self.movement_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }