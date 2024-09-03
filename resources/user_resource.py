from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError
from .models import db, User
import bcrypt

# Set up argument parser
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

        # Hash the password before storing
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(email=email, password_hash=password_hash, profile_picture=profile_picture)

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'A user with this email already exists.'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500

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

    def put(self, user_id):
        return self._update_user(user_id, partial=False)

    def patch(self, user_id):
        return self._update_user(user_id, partial=True)

    def _update_user(self, user_id, partial):
        args = user_parser.parse_args()
        email = args['email'] if not partial or args['email'] else None
        password = args['password'] if not partial or args['password'] else None
        profile_picture = args.get('profile_picture') if not partial or args['profile_picture'] else None

        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404

        if email:
            user.email = email
        if password:
            user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if profile_picture:
            user.profile_picture = profile_picture
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500

        return {
            'message': 'User profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'profile_picture': user.profile_picture,
                'created_at': user.created_at
            }
        }, 200
