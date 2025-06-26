
from flask import Blueprint, request, jsonify
from app.models import db, Inventory, Product
from flask import current_app
import os, json


inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('', methods=['GET'])
def get_inventory():
    item_id = request.args.get('id', type=int)

    if item_id:
        item = Inventory.query.get(item_id)
        if not item:
            return jsonify({'error': 'Inventory item not found'}), 404

        return jsonify({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name if item.product else None,
            'quantity': item.quantity,
            'location': item.location
        }), 200

    else:
        inventory_items = Inventory.query.all()
        return jsonify([
            {
                'id': i.id,
                'product_id': i.product_id,
                'product_name': i.product.name if i.product else None,
                'quantity': i.quantity,
                'location': i.location
            } for i in inventory_items
        ]), 200



@inventory_bp.route('/<int:id>', methods=['POST'])
def create_or_update_inventory(id):
    data = request.get_json()
    item = Inventory.query.get(id)

    if item:
        item.product_id = data.get('product_id', item.product_id)
        item.quantity = data.get('quantity', item.quantity)
        item.location = data.get('location', item.location)
    else:
        item = Inventory(
            id=id,
            product_id=data['product_id'],
            quantity=data['quantity'],
            location=data.get('location', '')
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Inventory item created or updated'}), 200

@inventory_bp.route('/load', methods=['POST'])
def load_inventory_from_file():
    
    file_path = os.path.join(current_app.root_path, 'data', 'inventory.json')

    try:
        with open(file_path, 'r') as f:
            items = json.load(f)

        for item in items:
            existing = Inventory.query.get(item['id'])
            if existing:
                existing.product_id = item['product_id']
                existing.quantity = item['quantity']
                existing.location = item.get('location', '')
            else:
                new_item = Inventory(**item)
                db.session.add(new_item)

        db.session.commit()
        return jsonify({'message': 'Inventory loaded from file'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
