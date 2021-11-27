import pytest
from src.api.models import Trade
from src import create_app, db


@pytest.fixture(scope='function')
def add_trade():
    def _add_trade(type_trade, user_id, symbol, shares, price, timestamp):
        trade = Trade(type_trade=type_trade, user_id=user_id, symbol=symbol,
                      shares=shares, price=price, timestamp=timestamp)
        db.session.add(trade)
        db.session.commit()
        return trade
    return _add_trade


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
