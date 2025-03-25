from db import db
from User import User
from flask import Flask
from config import Config
from flask_cors import CORS
from Methods import Methods
from decorators import admin_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

app=Flask(__name__)
app.config.from_object(Config)

# Modelagem
# Banco de dados
db.init_app(app)

# Autenticação de usuario.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

# Configuração para utilizar o swagger, para permitir que outros sistemas de fora possam acessar esse sistema.
CORS(app)
methods=Methods()

# Cadastro de usuario
@app.route('/registration-admin', methods=["POST"])
def registration_admin():
    return methods.registration_admin()

@app.route('/registration', methods=["POST"])
def registration_user():
    return methods.registration_user()

# Rota de autenticação configurado para o login_required, essa função carrega o usuario autenticado pora o @login_required
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login do usuario
@app.route('/login', methods=["POST"])
def login():
    return methods.login()

# Logout do usuario
@app.route('/logout', methods=["POST"])    
def logout():
    return methods.logout()

# Adicionando porduto
@app.route('/api/products/add', methods=["POST"])
@login_required
@admin_required
def add_products():
    return methods.add_products()

#Deletando produro
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
@admin_required
def delete_product(product_id):
    return methods.delete_product(product_id)

# Buscanndo o porduto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    return methods.get_product_details(product_id)

# Atualiza produto 
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
@admin_required
def upade_product(product_id):
    return methods.upade_product(product_id)

# Apresentar todos os produtos
@app.route('/api/products', methods=["GET"])
def get_products():
    return methods.get_products()

# Adicionar o produto no carrinho
@app.route('/api/cart/add/<int:product_id>', methods=["POST"])
@login_required
def add_to_cart(product_id):
    return methods.add_to_cart(product_id)

# Remover o produto do carrinho
@app.route('/api/cart/remove/<int:product_id>', methods=["DELETE"])
@login_required
def remove_from_car(product_id):
    return methods.remove_from_car(product_id)

# Listar todos os produtos no carrinho
@app.route('/api/cart', methods=["GET"])
@login_required
def view_cat():
    return methods.view_cat()

# Finalizar as comprar do carrinho, remove todos os  produtos do carrinho
@app.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
    return methods.checkout()

if __name__=="__main__":
    app.run(debug=True)