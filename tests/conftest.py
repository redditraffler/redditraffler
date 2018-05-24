from app.config import TestConfig
from app.factory import create_app
from app.extensions import db as _db
from app.db.models import Raffle, User
import pytest


@pytest.fixture(scope='session')
def app():
    test_app = create_app(TestConfig)
    context = test_app.app_context()
    context.push()
    yield test_app
    context.pop()


@pytest.fixture(scope='session')
def db(app, request):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function')
def db_session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def user(db_session):
    user = User(username='test_user')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def raffle(db_session, user):
    raffle = Raffle(submission_id='test_id',
                    submission_title='test_title',
                    submission_author='test_author',
                    subreddit='test_subreddit',
                    winner_count=1,
                    min_account_age=0,
                    min_comment_karma=0,
                    min_link_karma=0,
                    user_id=user.id)
    db_session.add(raffle)
    db_session.commit()
    return raffle
