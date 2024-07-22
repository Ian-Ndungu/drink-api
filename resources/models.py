from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
