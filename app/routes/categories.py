from flask import Blueprint, request, jsonify, current_app
from app.models import db, Category
import os
import json

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([
        {
            'id': c.id,
            'name': c.name
        } for c in categories
    ])


@category_bp.route('/<int:id>', methods=['POST'])
def create_or_update_category(id):
    data = request.get_json()
    category = Category.query.get(id)

    if category:
        category.name = data.get('name', category.name)
    else:
        category = Category(id=id, name=data['name'])
        db.session.add(category)

    db.session.commit()
    return jsonify({'message': 'Category created or updated'}), 200


@category_bp.route('/load', methods=['POST'])
def load_categories_from_file():
    file_path = os.path.join(current_app.root_path, 'data', 'categories.json')

    try:
        with open(file_path, 'r') as f:
            categories = json.load(f)

        for item in categories:
            category = Category.query.get(item['id'])
            if category:
                category.name = item['name']
            else:
                new_category = Category(**item)
                db.session.add(new_category)

        db.session.commit()
        return jsonify({'message': 'Categories loaded from JSON file'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
