from db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # isAdmin = db.Column(db.String(80), nullable=False)  # Define se o usuário é admin
    cart=db.relationship('CartIntem', backref='user', lazy=True)
