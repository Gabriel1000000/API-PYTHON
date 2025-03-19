from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app=Flask(__name__)
app.config['SECRET_KEY']='minha_chave'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecommerce.db'

# Modelagem
# Banco de dados
db = SQLAlchemy(app)
# Autenticação de usuario.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
# Configuração para utilizar o swagger, para permitir que outros sistemas de fora possam acessar esse sistema.
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart=db.relationship('CartIntem', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


class CartIntem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(80), db.ForeignKey('product.id'), nullable=False)
    
    

# Rota de autenticação configurado para o login_required, essa sunção carrega o usuario autenticado pora o @login_required
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login do usuario
@app.route('/login', methods=["POST"])
def login():
    data=request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    
    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message":"Logged in successfully"})    
    
    return jsonify({"message":"Unauthorized. Invalid credentials"}), 401

@app.route('/logout', methods=["POST"])    
def logout():
    logout_user()
    return jsonify({"message":"Logout successfully"})
# Adicionando porduto
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_products():
    data = request.json
    if 'name' in data and 'price' in data:
        product=Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product added successfully"})
    return jsonify({"message":"Invalid product data"}), 400

#Deletando produro
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    #Recuperar o produto da base de dados
    # Verificar se o porduto existe
    #Se existe, apagar da base de dado
    #Se não existe, retornar 404 not found
    product=Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"})
    return jsonify({"message":"Product not found"}), 404

# Buscanndo o porduto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product=Product.query.get(product_id)
    if product:
        return jsonify({
            "id" :product.id,
            "name" :product.name,
            "price" :product.price,
            "description" :product.description
        })
    return jsonify({"message":"Product not found"}), 400

# Atualiza produto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def upade_product(product_id):

    product= Product.query.get(product_id)
    
    if not product:
        return jsonify({"message":"Product not found"}), 404
    
    data=request.json
    if "name" in  data:
        product.name=data['name']

    if "price" in  data:
        product.price=data['price']

    if "description" in  data:
        product.description=data['description']

    db.session.commit()

    return  jsonify({"message":"Product updated successfully"})

# Apresentar todos os produtos
@app.route('/api/products', methods=["GET"])
def get_products():
    products=Product.query.all()
    # if products:
    products_list=[]
    for product in products:
        product_data={
                "id" :product.id,
                "name" :product.name,
                "price" :product.price
            }
        products_list.append(product_data)
    return jsonify(products_list)
    # return jsonify({"message":"Product not found"}), 400

@app.route('/api/cart/add/<int:product_id>', methods=["POST"])
@login_required
def add_to_cart(product_id):
    # User
    user=User.query.get(int(current_user.id))
    # Porduct
    product=Product.query.get(product_id)

    if user and product:
        cart_item= CartIntem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to the car sucessfully'})
    return jsonify({'message': 'Failed to add item to the cart'}), 400

@app.route('/api/cart/remove/<int:product_id>', methods=["DELETE"])
@login_required
def remove_from_car(product_id):
    cart_item=CartIntem.query.filter_by(user_id=current_user.id,product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message':'Item removed from the cart successfully'})
    return jsonify({'message':'Failed to remove item from the cart'}), 400

@app.route('/api/cart', methods=["GET"])
@login_required
def view_cat():
    user= User.query.get(int(current_user.id))
    cart_items=user.cart
    cart_content=[]
    for cart_item in cart_items:
        product=Product.query.get(cart_item.product_id)
        cart_content.append({
            'id': cart_item.id,
            'user_id':cart_item.user_id,
            'product_id': cart_item.product_id,
            'product_name': product.name,
            'product_price': product.price
        })
    return jsonify(cart_content)

@app.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
    user=User.query.get(int(current_user.id))
    cart_items=user.cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message':'Checkout successful. Cart has been cleared.'})

if __name__=="__main__":
    app.run(debug=True)