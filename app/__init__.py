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
    app.config.from_pyfile('../.env')

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)

    from app.routes.warehouse_routes import warehouse_bp
    from app.routes.product_routes import product_bp
    app.register_blueprint(warehouse_bp, url_prefix='/warehouses')
    app.register_blueprint(product_bp, url_prefix='/products')

    return app

