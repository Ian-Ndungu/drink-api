from flask_restful import Resource, reqparse
from .models import db, User

user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')
user_parser.add_argument('profile_picture', type=str, help='Profile picture URL')

class UserResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        email = args['email']
        password = args['password']
        profile_picture = args.get('profile_picture')

        # Hash the password before storing (not shown here; use a library like bcrypt)
        password_hash = password  # Replace with actual hashed password

        new_user = User(email=email, password_hash=password_hash, profile_picture=profile_picture)
        db.session.add(new_user)
        db.session.commit()

        return {
            'message': 'User profile created successfully',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'profile_picture': new_user.profile_picture,
                'created_at': new_user.created_at
            }
        }, 201

    def get(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'email': user.email,
            'profile_picture': user.profile_picture,
            'created_at': user.created_at
        }, 200
