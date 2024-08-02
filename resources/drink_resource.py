from flask_restful import Resource, reqparse
from resources.models import db, Drink

# Define a request parser to extract data from the request
drink_parser = reqparse.RequestParser()
drink_parser.add_argument('name', type=str, required=True, help='Name of the drink is required')
drink_parser.add_argument('image_url', type=str, required=True, help='Image URL of the drink is required')
drink_parser.add_argument('price', type=float, required=True, help='Price of the drink is required') 

class DrinkList(Resource):
    def get(self):
        # Get all drinks from the database
        drinks = Drink.query.all()
        return [
            {
                'id': drink.id, 
                'name': drink.name, 
                'image_url': drink.image_url,
                'price': drink.price  
            } 
            for drink in drinks
        ], 200

    def post(self):
        # Parse the incoming request data
        args = drink_parser.parse_args()
        name = args['name']
        image_url = args['image_url']
        price = args['price']  

        # Create a new Drink object and add it to the database
        new_drink = Drink(name=name, image_url=image_url, price=price) 
        db.session.add(new_drink)
        db.session.commit()

        return {
            'message': 'Drink added successfully', 
            'drink': {
                'id': new_drink.id, 
                'name': new_drink.name, 
                'image_url': new_drink.image_url,
                'price': new_drink.price  
            }
        }, 201

class DrinkResource(Resource):
    def get(self, drink_id):
        # Get a specific drink by ID
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404
        return {
            'id': drink.id, 
            'name': drink.name, 
            'image_url': drink.image_url,
            'price': drink.price  
        }, 200

    def put(self, drink_id):
        # Update a drink by ID
        args = drink_parser.parse_args()
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404

        drink.name = args['name']
        drink.image_url = args['image_url']
        drink.price = args['price']  
        db.session.commit()
        return {
            'message': 'Drink updated successfully', 
            'drink': {
                'id': drink.id, 
                'name': drink.name, 
                'image_url': drink.image_url,
                'price': drink.price  
            }
        }, 200

    def delete(self, drink_id):
        # Delete a drink by ID
        drink = Drink.query.get(drink_id)
        if drink is None:
            return {'message': 'Drink not found'}, 404

        db.session.delete(drink)
        db.session.commit()
        return {'message': 'Drink deleted successfully'}, 200
