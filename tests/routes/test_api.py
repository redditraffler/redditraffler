from flask import url_for, session
from app.util import reddit


def test_submissions_no_token(client):
    res = client.get(url_for('api.submissions'))
    assert res.status_code == 401


def test_submissions(client, monkeypatch):
    with client.session_transaction() as session:
        session['reddit_refresh_token'] = 'test_token'

    monkeypatch.setattr(reddit, 'get_user_submissions', lambda x: [])

    res = client.get(url_for('api.submissions'))
    assert res.status_code == 200


def test_submission_no_params(client):
    res = client.get(url_for('api.submission'))
    assert res.status_code == 400


def test_submission_invalid_submission(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: None)
    res = client.get(url_for('api.submission', url='some_url'))
    assert res.status_code == 404


def test_submission(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_id: 'nonempty')
    res = client.get(url_for('api.submission', id='some_id'))
    assert res.status_code == 200
