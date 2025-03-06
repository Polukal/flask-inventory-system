from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
import os

db = SQLAlchemy()
migrate = Migrate()
redis_client = FlaskRedis()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.utils.config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models.warehouse import Warehouse
    from app.models.product import Product
    from app.models.stock_movement import StockMovement
    
    # Register blueprints
    from app.routes.warehouse_routes import warehouse_bp
    from app.routes.product_routes import product_bp
    from app.routes.alerts import alerts_bp
    
    app.register_blueprint(warehouse_bp, url_prefix='/warehouses')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(alerts_bp, url_prefix='/alerts')
    
    # Create a context for database creation/migration when using Flask CLI
    with app.app_context():
        db.create_all()
    
    return app