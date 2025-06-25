
from flask import Blueprint, request, jsonify, current_app
from app.models import db, Product
import os
import json

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'category_id': p.category_id
        } for p in products
    ])


@product_bp.route('/<int:id>', methods=['POST'])
def create_or_update_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if product:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)
    else:
        product = Product(
            id=id,
            name=data['name'],
            price=data['price'],
            category_id=data['category_id']
        )
        db.session.add(product)

    db.session.commit()
    return jsonify({'message': 'Product created or updated'}), 200


@product_bp.route('/load', methods=['POST'])
def load_products_from_file():
    file_path = os.path.join(current_app.root_path, 'data', 'products.json')
    
    try:
        with open(file_path, 'r') as f:
            products = json.load(f)

        for item in products:
            product = Product.query.get(item['id'])
            if product:
                product.name = item['name']
                product.price = item['price']
                product.category_id = item['category_id']
            else:
                new_product = Product(**item)
                db.session.add(new_product)

        db.session.commit()
        return jsonify({'message': 'Products loaded from JSON file'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
