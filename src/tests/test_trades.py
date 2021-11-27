import json

from src.api.models import Trade


def test_create_trade(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        '/trades',
        data=json.dumps({
            'type_trade': 'buy',
            'user_id': 1,
            'symbol': 'USD',
            'shares': 30,
            'price': 90,
            'timestamp':1531522701000
        }),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert 'New trade of type: buy with user id: ' \
           '1 and price: 90 was added!' in data['message']


def test_single_trade(test_app, test_database, add_trade):
    trade = add_trade(type_trade='sell', user_id=1, symbol='ABX', shares=30,
                      price=134, timestamp=1531522701000)
    client = test_app.test_client()
    response = client.get(f'/trades/{trade.id}')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'sell' == data['type_trade']
    assert 1 == data['user_id']
    assert 'ABX' == data['symbol']
    assert 30 == data['shares']
    assert 134 == data['price']
    assert 1531522701000 == data['timestamp']


def test_single_trade_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    response = client.get('/trades/999')
    data = json.loads(response.data.decode())
    assert response.status_code == 404
    assert 'Trade 999 does not exist' in data['message']


def test_all_trades(test_app, test_database, add_trade):

    add_trade(type_trade='buy', user_id=1, symbol='ABX', shares=30,
                      price=134, timestamp=1531522701000)
    add_trade(type_trade='sell', user_id=2, symbol='USD', shares=10,
                      price=200, timestamp=1531522701987)
    add_trade(type_trade='sell', user_id=3, symbol='COL', shares=35,
                      price=407, timestamp=1531522701345)

    client = test_app.test_client()
    response = client.get(f'/trades')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 5
    assert 1 == data[0]['id']
    assert 2 == data[1]['id']
    assert 3 == data[2]['id']
    assert 4 == data[3]['id']
    assert 5 == data[4]['id']


def test_remove_trade(test_app, test_database, add_trade):
    test_database.session.query(Trade).delete()
    trade = add_trade(type_trade='sell', user_id=1, symbol='ABX', shares=30,
                      price=134, timestamp=1531522701000)
    client = test_app.test_client()
    resp_one = client.get('/trades')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f'/trades/{trade.id}')
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 405
    assert len(data) == 1


def test_put_trade(test_app, test_database, add_trade):
    test_database.session.query(Trade).delete()
    trade = add_trade(type_trade='sell', user_id=1, symbol='ABX', shares=30,
                      price=134, timestamp=1531522701000)
    client = test_app.test_client()
    resp_one = client.put(f'/trades/{trade.id}',
                          data=json.dumps(
                              {'type_trade': 'buy', 'symbol': 'USD'}),
                          content_type='application/json',
                          )
    json.loads(resp_one.data.decode())
    assert resp_one.status_code == 405

    resp_two = client.get(f'/trades/{trade.id}')
    data = json.loads(resp_two.data.decode())
    assert 'sell' == data['type_trade']
    assert 'ABX' == data['symbol']