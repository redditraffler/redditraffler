import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.db.models.user import User
from app.extensions import db


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"TestUser{n}")
