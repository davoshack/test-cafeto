
```
(env) ➜  test-cafeto-api-rest git:(master) ✗ docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src"
============================================================================= test session starts ==============================================================================
platform linux -- Python 3.9.5, pytest-6.2.4, py-1.11.0, pluggy-0.13.1
rootdir: /usr/src/app/src/tests, configfile: pytest.ini
plugins: cov-2.12.0
collected 8 items                                                                                                                                                              

src/tests/test_config.py ..                                                                                                                                              [ 25%]
src/tests/test_trades.py ......                                                                                                                                          [100%]

----------- coverage: platform linux, python 3.9.5-final-0 -----------
Name                  Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------
src/__init__.py          15      1      0      0    93%
src/api/__init__.py       0      0      0      0   100%
src/api/models.py        18      0      2      0   100%
src/api/trade.py         33      0      6      0   100%
src/config.py            10      0      6      0   100%
-------------------------------------------------------
TOTAL                    76      1     14      0    99%


============================================================================== 8 passed in 0.87s ===============================================================================
```


# Python Flask: Stock Trades API

## Question description

In this challenge, your task is to implement a simple REST API to manage a collection of stock trades.

Each trade has the following structure:

- `id`: The unique ID of the trade. (Integer)
- `type`: The type of the trade, either 'buy' or 'sell'. (String)
- `user_id`: The unique user ID. (Integer)
- `symbol`: The stock symbol of the trade. (String)
- `shares`: The total number of shares traded. The traded shares value is between 10 and 30 shares, inclusive. (Integer)
- `price`: The price of one share of stock at the time of the trade. (Integer)
- `timestamp`: The epoch time of the stock trade in milliseconds. (Integer)


### Example of a trade data JSON object:
```
{
    "id": 1,
    "type": "buy",
    "user_id": 23,
    "symbol": "ABX",
    "shares": 30,
    "price": 134,
    "timestamp": 1531522701000
}
```

## Requirements:

You are provided with the implementation of the Trade model. The REST service must expose the `/trades` endpoint, which allows for managing the collection of trade records in the following way:

`POST /trades`:

- creates a new trade
- expects a JSON trade object without an id property as a body payload. You can assume that the given object is always valid.
- adds the given trade object to the collection of trades and assigns a unique integer id to it. The first created trade must have id 1, the second one 2, and so on.
- the response code is 201, and the response body is the created trade object

`GET /trades`:

- returns a collection of all trades
- the response code is 200, and the response body is an array of all trade objects ordered by their ids in increasing order

`GET /trades/<id>`:

- returns a trade with the given id
- if the matching trade exists, the response code is 200 and the response body is the matching trade object
- if there is no trade with the given id in the collection, the response code is 404

`DELETE`, `PUT`, `PATCH` request to `/trades/<id>`:

- the response code is 405 because the API does not allow deleting or modifying trades for any id value
