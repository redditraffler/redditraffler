import pytest

from app.config import TestConfig
from app.factory import create_app
from app.extensions import db as _db
from app.db.models import raffle, user, winner


@pytest.fixture(scope="session")
def app():
    test_app = create_app(TestConfig)
    with test_app.app_context():
        yield test_app


@pytest.fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def db_session(db):
    connection = db.engine.connect()
    session = db.session
    yield session
    connection.close()
    session.remove()


@pytest.fixture(scope="class", autouse=True)
def truncate_db_after_each_class(db):
    """ Reset the test DB to a clean slate after each class. """
    models = [winner.Winner, raffle.Raffle, user.User]  # Specify models with FKs first
    for model in models:
        db.session.query(model).delete()
    db.session.commit()


@pytest.fixture
def authed_client(client, db_session, mocker):
    with client.session_transaction() as session:
        session["jwt"] = "some_jwt"
        session["reddit_username"] = "some_username"

    jwt_decode = mocker.patch("app.util.jwt_helper.decode")
    jwt_decode.return_value = {"user_id": 9999, "username": "redditraffler-test"}
    yield client
