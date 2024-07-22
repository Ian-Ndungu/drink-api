from flask_restful import Resource, reqparse
from .models import db, Drink

class DrinkResource(Resource):
    def get(self, drink_id):
        drink = Drink.query.get_or_404(drink_id)
        return {'id': drink.id, 'name': drink.name, 'image_url': drink.image_url, 'price': drink.price}

    def delete(self, drink_id):
        drink = Drink.query.get_or_404(drink_id)
        db.session.delete(drink)
        db.session.commit()
        return '', 204

class DrinkList(Resource):
    def get(self):
        drinks = Drink.query.all()
        return [{'id': drink.id, 'name': drink.name, 'image_url': drink.image_url, 'price': drink.price} for drink in drinks]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str, help="Name of the drink")
        parser.add_argument('image_url', required=True, type=str, help="Image URL of the drink")
        parser.add_argument('price', required=True, type=float, help="Price of the drink")
        args = parser.parse_args()

        new_drink = Drink(name=args['name'], image_url=args['image_url'], price=args['price'])
        db.session.add(new_drink)
        db.session.commit()
        return {'id': new_drink.id, 'name': new_drink.name, 'image_url': new_drink.image_url, 'price': new_drink.price}, 201
