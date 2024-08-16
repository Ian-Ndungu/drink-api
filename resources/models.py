from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    customer_email = db.Column(db.String(80), nullable=False)
    order_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    drink = db.relationship('Drink', back_populates='orders')
    user = db.relationship('User', backref='orders')

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship('Order', order_by=Order.id, back_populates='drink')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    orders = db.relationship('Order', backref='user', lazy=True)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_customer = db.Column(db.Boolean, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message id={self.id} text={self.text} is_customer={self.is_customer} is_read={self.is_read}>"
