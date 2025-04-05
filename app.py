from flask import Flask, render_template
from flasgger import Swagger
from models.database import db
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

swagger = Swagger(app)  # Initialize Swagger
db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
