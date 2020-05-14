import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.db.models.user import User
from tests.helpers import scoped_session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = scoped_session

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"TestUser{n}")
