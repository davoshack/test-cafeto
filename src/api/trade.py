from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import Trade


trades_blueprint = Blueprint('trades', __name__)
api = Api(trades_blueprint)

trade = api.model('Trade', {
    'id': fields.Integer(readOnly=True),
    'type_trade': fields.String(required=True),
    'user_id': fields.Integer(required=True),
    'symbol': fields.String(required=True),
    'shares': fields.Integer(required=True),
    'price': fields.Integer(required=True),
    'timestamp': fields.Integer(required=True),
})


class Trades(Resource):

    @api.marshal_with(trade)
    def get(self, trade_id):
        trade = Trade.query.filter_by(id=trade_id).first()
        if not trade:
            api.abort(404, f'Trade {trade_id} does not exist')
        return trade, 200


class TradeList(Resource):

    @api.marshal_with(trade, as_list=True)
    def get(self):
        return Trade.query.order_by(Trade.id.asc()).all()

    @api.expect(trade, validate=True)
    def post(self):
        post_data = request.get_json()

        type_trade = post_data.get('type_trade')
        user_id = post_data.get('user_id')
        symbol = post_data.get('symbol')
        shares = post_data.get('shares')
        price = post_data.get('price')
        timestamp = post_data.get('timestamp')

        db.session.add(Trade(type_trade=type_trade,
                             user_id=user_id,
                             symbol=symbol,
                             shares=shares,
                             price=price,
                             timestamp=timestamp))
        db.session.commit()

        response_object = {
            'message': f'New trade of type: {type_trade} with user id: {user_id}'
                       f' and price: {price} was added!'
        }
        return response_object, 201


api.add_resource(TradeList, '/trades')
api.add_resource(Trades, '/trades/<int:trade_id>')
