from flask import url_for, session
from app.util import reddit
from app.routes import api
from app.jobs.raffle_job import raffle


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


def test_post_new_raffle_no_params(client):
    assert client.post(url_for('api.new_raffle')).status_code == 422


def test_post_new_raffle_invalid_params(client):
    res = client.post(url_for('api.new_raffle'), data=_invalid_form_params())
    assert res.status_code == 422


def test_post_new_raffle_valid_params(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: True)
    monkeypatch.setattr(api, '_raffle_exists', lambda sub_url: False)
    monkeypatch.setattr(raffle, 'queue', _stub_raffle_job)
    params = _valid_form_params()
    res = client.post(url_for('api.new_raffle'), data=_valid_form_params())
    assert res.status_code == 202


def test_post_new_raffle_valid_params_existing_raffle(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: True)
    monkeypatch.setattr(api, '_raffle_exists', lambda sub_url: True)
    monkeypatch.setattr(raffle, 'queue', _stub_raffle_job)
    params = _valid_form_params()
    res = client.post(url_for('api.new_raffle'), data=_valid_form_params())
    assert res.status_code == 303


def _valid_form_params():
    return {
        'submissionUrl': 'https://redd.it/57xvjb',
        'winnerCount': 1,
        'minAge': 0,
        'minComment': 0,
        'minLink': 0
    }


def _invalid_form_params():
    return _valid_form_params().update({'winnerCount': 0})


def _stub_raffle_job(raffle_params, user, job_id):
    return [raffle_params, user, job_id]
