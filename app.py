from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, but recommended

    db.init_app(app)

    # Initialize CORS
    CORS(app)

    from resources.drink_resource import DrinkResource, DrinkList

    api.add_resource(DrinkResource, '/api/drinks/<int:drink_id>')
    api.add_resource(DrinkList, '/api/drinks')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
