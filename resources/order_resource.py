from flask_restful import Resource, reqparse
from .models import db, Order

# Order parser
order_parser = reqparse.RequestParser()
order_parser.add_argument('drink_id', type=int, required=True, help='Drink ID is required')
order_parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
order_parser.add_argument('customer_email', type=str, required=True, help='Customer email is required')

class OrderResource(Resource):
    def post(self):
        args = order_parser.parse_args()
        drink_id = args['drink_id']
        quantity = args['quantity']
        customer_email = args['customer_email']

        new_order = Order(drink_id=drink_id, quantity=quantity, customer_email=customer_email)
        db.session.add(new_order)
        db.session.commit()

        return {
            'message': 'Order created successfully',
            'order': {
                'id': new_order.id,
                'drink_id': new_order.drink_id,
                'quantity': new_order.quantity,
                'customer_email': new_order.customer_email,
                'order_time': new_order.order_time
            }
        }, 201

    def get(self, order_id):
        order = Order.query.get(order_id)
        if order is None:
            return {'message': 'Order not found'}, 404

        return {
            'id': order.id,
            'drink_id': order.drink_id,
            'quantity': order.quantity,
            'customer_email': order.customer_email,  
            'order_time': order.order_time
        }, 200
