from app.factory import create_app
from app.db import db as _db
import pytest

settings = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db'
}


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update(settings)
    context = app.app_context()
    context.push()
    yield app
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
