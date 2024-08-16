from flask_restful import Resource, reqparse
from .models import db, Order

# Order parser
order_parser = reqparse.RequestParser()
order_parser.add_argument('drink_id', type=int, required=True, help='Drink ID is required')
order_parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
order_parser.add_argument('customer_name', type=str, required=True, help='Customer name is required')

class OrderResource(Resource):
    def post(self):
        args = order_parser.parse_args()
        drink_id = args['drink_id']
        quantity = args['quantity']
        customer_name = args['customer_name']

        new_order = Order(drink_id=drink_id, quantity=quantity, customer_name=customer_name)
        db.session.add(new_order)
        db.session.commit()

        return {
            'message': 'Order created successfully',
            'order': {
                'id': new_order.id,
                'drink_id': new_order.drink_id,
                'quantity': new_order.quantity,
                'customer_name': new_order.customer_name,
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
            'customer_name': order.customer_name,
            'order_time': order.order_time
        }, 200
