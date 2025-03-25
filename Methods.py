from db import db
from User import User
from Product import Product
from CartIntem import CartIntem
from flask import request, jsonify
from flask_login import login_user, logout_user, current_user


class Methods:

    
    def registration_admin(self):
        data=request.json
        if 'username' in data:
            admin=User(username=data['username'], password=data['password'], is_admin=data['is_admin'])
            db.session.add(admin)
            db.session.commit()
            return jsonify({'message':'Registered successfully.'})
        return jsonify({'message':'User already exists.'}), 409
    
    def registration_user(self):
        data=request.json
            # Verifica se os campos obrigatórios estão na requisição
        if 'username' not in data or not data['username'].strip():
            return jsonify({'message': 'Username cannot be empty.'}), 400

        if 'password' not in data or not data['password'].strip():
            return jsonify({'message': 'Password cannot be empty.'}), 400

        # Verifica se o usuário já existe no banco
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'message': 'User already exists.'}), 409
        
        admin=User(username=data['username'], password=data['password'])
        db.session.add(admin)
        db.session.commit()
        return jsonify({'message':'Registered successfully.'})
        return jsonify({'message':'User already exists.'}), 409

    def registration_user(self):
        data=request.json
            # Verifica se os campos obrigatórios estão na requisição
        if 'username' not in data or not data['username'].strip():
            return jsonify({'message': 'Username cannot be empty.'}), 400

        if 'password' not in data or not data['password'].strip():
            return jsonify({'message': 'Password cannot be empty.'}), 400

        # Verifica se o usuário já existe no banco
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'message': 'User already exists.'}), 409

        # Cria um novo usuário
        user = User(username=data['username'], password=data['password']) 
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Registered successfully.'}), 201
    
    def login(self):
        data=request.json
        
        user = User.query.filter_by(username=data.get("username")).first()
        
        if user and data.get("password") == user.password:
                login_user(user)
                return jsonify({"message":"Logged in successfully"})    
        
        return jsonify({"message":"Unauthorized. Invalid credentials"}), 401
    
    def logout(self):
        logout_user()
        return jsonify({"message":"Logout successfully"})
    
    # Adicionando porduto
    def add_products(self):
        data = request.json
        if 'name' in data and 'price' in data:
            product=Product(name=data["name"], price=data["price"], description=data.get("description", ""))
            db.session.add(product)
            db.session.commit()
            return jsonify({"message":"Product added successfully"})
        return jsonify({"message":"Invalid product data"}), 400

    #Deletando produro
    def delete_product(self,product_id):
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
    def get_product_details(self,product_id):
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
    def upade_product(self,product_id):

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
    def get_products(self):
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
    

    def add_to_cart(self,product_id):
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

    
    def remove_from_car(self,product_id):
        cart_item=CartIntem.query.filter_by(user_id=current_user.id,product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'message':'Item removed from the cart successfully'})
        return jsonify({'message':'Failed to remove item from the cart'}), 400

    
    def view_cat(self):
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

    
    def checkout(self):
        user=User.query.get(int(current_user.id))
        cart_items=user.cart
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message':'Checkout successful. Cart has been cleared.'})