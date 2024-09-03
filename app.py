from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from resources.models import db
from resources.drink_resource import DrinkList, DrinkResource, DrinkCategoryResource
from resources.order_resource import OrderResource
from resources.user_resource import UserResource
from resources.chat_resource import ChatResource

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register resources
    api = Api(app)
    api.add_resource(DrinkResource, '/api/drinks/<int:drink_id>')
    api.add_resource(DrinkList, '/api/drinks')
    api.add_resource(DrinkCategoryResource, '/api/drinks/category/<string:category>')
    api.add_resource(OrderResource, '/api/orders', '/api/orders/<int:order_id>')
    api.add_resource(UserResource, '/api/users')
    api.add_resource(ChatResource, '/api/messages', '/api/messages/<int:message_id>')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
