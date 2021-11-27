import sys

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import Trade


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    db.session.add(Trade(type_trade='buy', user_id=1, symbol='ABX', shares=30,
                         price=134, timestamp=1531522701000))
    db.session.add(Trade(type_trade='sell', user_id=2, symbol='USD', shares=10,
                         price=200, timestamp=1531522701987))
    db.session.add(Trade(type_trade='sell', user_id=3, symbol='COL', shares=35,
                         price=407, timestamp=1531522701345))
    db.session.commit()


if __name__ == '__main__':
    cli()
