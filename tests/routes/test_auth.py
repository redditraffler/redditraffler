from flask import url_for, session
from app.util import reddit
from app.db.models import User


def test_logout(client):
    res = client.post(url_for('auth.logout'))
    assert not session
    assert res.status_code == 302


def test_auth_redirect_access_denied(client):
    """ Assert that an error is shown. """
    params = {'error': 'access_denied'}
    res = client.get(url_for('auth.auth_redirect'), query_string=params)
    assert res.status_code == 500


def test_auth_redirect_valid_token_existing_user(client, monkeypatch, session):
    """ Assert that a new user is not created and the user is redirected. """
    username = 'test_user'
    monkeypatch.setattr(reddit, 'authorize', lambda x: 'test_token')
    monkeypatch.setattr(reddit, 'get_username', lambda x: username)
    user = User(username=username)
    session.add(user)
    session.commit()
    res = client.get(url_for('auth.auth_redirect'))
    assert res.status_code == 302
    assert User.query.count() == 1
    assert User.query.first() == user


def test_auth_redirect_valid_token_new_user(client, monkeypatch, session):
    new_username = 'test_new_user'
    monkeypatch.setattr(reddit, 'authorize', lambda x: 'test_token')
    monkeypatch.setattr(reddit, 'get_username', lambda x: new_username)
    res = client.get(url_for('auth.auth_redirect'))
    assert res.status_code == 302
    assert User.query.first().username == new_username
