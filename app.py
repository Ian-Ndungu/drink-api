from flask import Flask, request, redirect, url_for, render_template, session
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from resources.models import db, User
from resources.drink_resource import DrinkResource, DrinkList

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  

    db.init_app(app)  # Initialize the database with the app
    CORS(app)  # Enable CORS
    api = Api(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    api.add_resource(DrinkResource, '/api/drinks/<int:drink_id>')
    api.add_resource(DrinkList, '/api/drinks')

    with app.app_context():
        db.create_all()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Invalid credentials'
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def index():
        return 'Welcome to the main page!'

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                return 'Username already exists'
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)  
