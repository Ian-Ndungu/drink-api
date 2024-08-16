from flask_restful import Resource, reqparse
from .models import db, Message

message_parser = reqparse.RequestParser()
message_parser.add_argument('text', type=str, required=True, help='Message text is required')
message_parser.add_argument('is_customer', type=bool, required=True, help='Indicates if the message is from the customer')

class ChatResource(Resource):
    def get(self):
        messages = Message.query.order_by(Message.timestamp.desc()).all()
        return [
            {
                'id': message.id,
                'text': message.text,
                'is_customer': message.is_customer,
                'is_read': message.is_read,
                'timestamp': message.timestamp
            }
            for message in messages
        ], 200

    def post(self):
        args = message_parser.parse_args()
        new_message = Message(
            text=args['text'],
            is_customer=args['is_customer']
        )
        db.session.add(new_message)
        db.session.commit()

        return {
            'message': 'Message sent successfully',
            'message_data': {
                'id': new_message.id,
                'text': new_message.text,
                'is_customer': new_message.is_customer,
                'is_read': new_message.is_read,
                'timestamp': new_message.timestamp
            }
        }, 201

    def put(self, message_id):
        message = Message.query.get(message_id)
        if not message:
            return {'message': 'Message not found'}, 404

        message.is_read = True
        db.session.commit()

        return {
            'message': 'Message marked as read',
            'message_data': {
                'id': message.id,
                'text': message.text,
                'is_customer': message.is_customer,
                'is_read': message.is_read,
                'timestamp': message.timestamp
            }
        }, 200
