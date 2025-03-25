from db import db

class CartIntem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(80), db.ForeignKey('product.id'), nullable=False)