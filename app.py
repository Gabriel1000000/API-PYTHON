from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecommerce.db'

# Modelagem
db = SQLAlchemy(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Adicionando porduto
@app.route('/api/products/add', methods=["POST"])
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



#Definir uma rota raiz (página inicial) e a função que será executada ao requisitar 
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