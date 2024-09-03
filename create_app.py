from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
    db.init_app(app)

    from resources.drink_resource import DrinkResource, DrinkList
    api.add_resource(DrinkResource, '/drinks/<int:drink_id>')
    api.add_resource(DrinkList, '/drinks')

    from resources.user_resource import UserResource,UserList
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(UserList, '/api/users')

    return app
