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


def test_submission_invalid_submission(client, monkeypatch, db_session):
    monkeypatch.setattr(reddit, 'submission_id_from_url', lambda x: None)
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: None)
    res = client.get(url_for('api.submission', url='some_url'))
    assert res.status_code == 404


def test_submission_existing_raffle(client, monkeypatch, db_session, raffle):
    monkeypatch.setattr(reddit, 'submission_id_from_url', lambda x: 'test_id')
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: None)
    res = client.get(url_for('api.submission', url='some_url'))
    assert res.status_code == 303


def test_submission_valid_submission(client, monkeypatch, db_session):
    monkeypatch.setattr(reddit, 'submission_id_from_url', lambda x: None)
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: 'something')
    res = client.get(url_for('api.submission', url='some_url'))
    assert res.status_code == 200
