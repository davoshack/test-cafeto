from sqlalchemy.sql import func

from src import db


class Trade(db.Model):

    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    type_trade = db.Column(db.String)
    user_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    shares = db.Column(db.Integer)
    price = db.Column(db.Integer)
    timestamp = db.Column(db.BigInteger)

    def __init__(self, type_trade, user_id, symbol, shares, price, timestamp):
        self.type_trade = type_trade
        self.user_id = user_id
        self.symbol = symbol
        self.shares = shares
        self.price = price
        self.timestamp = timestamp
