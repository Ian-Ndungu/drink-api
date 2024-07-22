from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.models import db
from resources.drink_resource import DrinkResource, DrinkList

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, but recommended

    db.init_app(app)  # Initialize the database with the app
    CORS(app)  # Enable CORS
    api = Api(app)

    api.add_resource(DrinkResource, '/api/drinks/<int:drink_id>')
    api.add_resource(DrinkList, '/api/drinks')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)  # Change port if needed
