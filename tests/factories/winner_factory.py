import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.db.models.winner import Winner
from app.extensions import db


class WinnerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Winner
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    raffle = factory.SubFactory("tests.factories.raffle_factory.RaffleFactory")

    username = factory.Faker("pystr", max_chars=10)
    account_age = factory.Faker("pyint", min_value=1, max_value=3650)
    comment_karma = factory.Faker("pyint", min_value=1, max_value=3650)
    link_karma = factory.Faker("pyint", min_value=1, max_value=3650)
    comment_url = factory.Faker("url")
