from flask_restful import Resource, reqparse
from app import db
from models import Drink

class DrinkResource(Resource):
    def get(self, drink_id):
        drink = Drink.query.get_or_404(drink_id)
        return drink.to_dict()

    def put(self, drink_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name of the drink')
        parser.add_argument('image_url', required=True, help='Image URL of the drink')
        parser.add_argument('price', type=float, required=True, help='Price of the drink')
        args = parser.parse_args()

        drink = Drink.query.get_or_404(drink_id)
        drink.name = args['name']
        drink.image_url = args['image_url']
        drink.price = args['price']
        db.session.commit()
        return drink.to_dict()

    def delete(self, drink_id):
        drink = Drink.query.get_or_404(drink_id)
        db.session.delete(drink)
        db.session.commit()
        return '', 204

class DrinkList(Resource):
    def get(self):
        drinks = Drink.query.all()
        return [drink.to_dict() for drink in drinks]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name of the drink')
        parser.add_argument('image_url', required=True, help='Image URL of the drink')
        parser.add_argument('price', type=float, required=True, help='Price of the drink')
        args = parser.parse_args()

        drink = Drink(name=args['name'], image_url=args['image_url'], price=args['price'])
        db.session.add(drink)
        db.session.commit()
        return drink.to_dict(), 201
