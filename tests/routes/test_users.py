from flask import url_for, session
from app.db.models import User


def test_show_user_valid_user(client, db_session):
    """ Assert that the user's profile page is shown. """
    username = 'test_user'
    user = User(username=username)
    db_session.add(user)
    db_session.commit()

    res = client.get(url_for('users.show_user', username=user.username))
    assert res.status_code == 200


def test_show_user_invalid_user(client, db_session):
    res = client.get(url_for('users.show_user', username='invalid'))
    assert res.status_code == 404
