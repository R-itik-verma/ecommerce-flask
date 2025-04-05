from flask import Blueprint, request, jsonify
from models.database import db
from models.cart import Cart
from models.product import Product
from flasgger import swag_from

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart', methods=['GET'])
@swag_from({
    'responses': {200: {'description': 'Cart items list'}},
    'tags': ['Cart']
})
def get_cart():
    cart_items = Cart.query.all()
    cart_list = [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]
    return jsonify(cart_list)

@cart_bp.route('/cart', methods=['POST'])
@swag_from({
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {'example': {'product_id': 1, 'quantity': 2}}
    }],
    'responses': {201: {'description': 'Product added to cart'}},
    'tags': ['Cart']
})
def add_to_cart():
    data = request.get_json()
    product = Product.query.get(data['product_id'])

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    cart_item = Cart(product_id=product.id, quantity=data.get('quantity', 1))
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product added to cart!'}), 201
