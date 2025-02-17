from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

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
    user = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Rota de autenticação configurado para o login_required, essa sunção carrega o usuario autenticado pora o @login_required
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login do usuario
@app.route('/login', methods=["POST"])
def login():
    data=request.json
    
    user=User.query.filter_by(user=data.get("user")).first()
    
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


# @app.route('/')
# def hello_wolrd():
#     return "Hello wolrd!!"

if __name__=="__main__":
    app.run(debug=True)