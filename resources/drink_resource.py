from flask_restful import Resource, reqparse
from resources.models import db, Drink

# Drink parser
drink_parser = reqparse.RequestParser()
drink_parser.add_argument('name', type=str, required=True, help='Name of the drink is required')
drink_parser.add_argument('image_url', type=str, required=True, help='Image URL of the drink is required')
drink_parser.add_argument('category', type=str, required=True, help='Category of the drink is required')
drink_parser.add_argument('price', type=float, required=True, help='Price of the drink is required')

class DrinkList(Resource):
    def get(self):
        drinks = Drink.query.all()
        return [
            {
                'id': drink.id, 
                'name': drink.name, 
                'image_url': drink.image_url,
                'category': drink.category,  
                'price': drink.price  
            } 
            for drink in drinks
        ], 200

    def post(self):
        args = drink_parser.parse_args()
        name = args['name']
        image_url = args['image_url']
        category = args['category']
        price = args['price']

        new_drink = Drink(name=name, image_url=image_url, category=category, price=price)
        db.session.add(new_drink)
        db.session.commit()

        return {
            'message': 'Drink added successfully', 
            'drink': {
                'id': new_drink.id, 
                'name': new_drink.name, 
                'image_url': new_drink.image_url,
                'category': new_drink.category, 
                'price': new_drink.price  
            }
        }, 201

class DrinkResource(Resource):
    def get(self, drink_id):
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404
        return {
            'id': drink.id, 
            'name': drink.name, 
            'image_url': drink.image_url,
            'category': drink.category,  
            'price': drink.price  
        }, 200

    def put(self, drink_id):
        args = drink_parser.parse_args()
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404

        drink.name = args['name']
        drink.image_url = args['image_url']
        drink.category = args['category'] 
        drink.price = args['price']  
        db.session.commit()
        return {
            'message': 'Drink updated successfully', 
            'drink': {
                'id': drink.id, 
                'name': drink.name, 
                'image_url': drink.image_url,
                'category': drink.category,  
                'price': drink.price  
            }
        }, 200

    def delete(self, drink_id):
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404

        db.session.delete(drink)
        db.session.commit()
        return {'message': 'Drink deleted successfully'}, 200

class DrinkCategoryResource(Resource):
    def get(self, category):
        drinks = Drink.query.filter_by(category=category).all()
        if not drinks:
            return {'message': f'No drinks found in category: {category}'}, 404

        return [
            {
                'id': drink.id, 
                'name': drink.name, 
                'image_url': drink.image_url,
                'category': drink.category, 
                'price': drink.price  
            } 
            for drink in drinks
        ], 200
