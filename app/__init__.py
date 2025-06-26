
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.products import product_bp
    from app.routes.categories import category_bp
    from app.routes.inventory import inventory_bp  

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')  

    return app

