from flask import Blueprint, request, jsonify
from models.database import db
from models.product import Product
from flasgger import swag_from

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
@swag_from({
    'responses': {200: {'description': 'List of products'}},
    'tags': ['Products']
})
def get_products():
    products = Product.query.all()
    product_list = [{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in products]
    return jsonify(product_list)

@product_bp.route('/products', methods=['POST'])
@swag_from({
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {'example': {'name': 'Laptop', 'price': 799.99, 'description': 'A powerful laptop'}}
    }],
    'responses': {201: {'description': 'Product added successfully'}},
    'tags': ['Products']
})
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], description=data.get('description', ''))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'}), 201


# from flask import Blueprint, request, jsonify, render_template
# from models.database import db
# from models.product import Product

# product_bp = Blueprint('product_bp', __name__)

# @product_bp.route('/add_product_form', methods=['GET'])
# def add_product_form():
#     return render_template('add_product.html')

# @product_bp.route('/products', methods=['POST'])
# def add_product():
#     if request.is_json:
#         data = request.get_json()
#     else:
#         data = request.form  # Get form data

#     new_product = Product(name=data['name'], price=float(data['price']), description=data.get('description', ''))
#     db.session.add(new_product)
#     db.session.commit()
#     return jsonify({'message': 'Product added successfully!'}), 201
from flask import Blueprint, request, jsonify, render_template
from models.database import db
from models.product import Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/add_product_form', methods=['GET'])
def add_product_form():
    return render_template('add_product.html')

@product_bp.route('/add_product_form', methods=['POST'])
def submit_product_form():
    data = request.form
    new_product = Product(name=data['name'], price=float(data['price']), description=data.get('description', ''))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

@product_bp.route('/products', methods=['GET'])
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)