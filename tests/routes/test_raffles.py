from flask import url_for, request
from app.util import reddit
from app.jobs.raffle_job import raffle
from rq.queue import Queue


def test_index(client, db_session):
    assert client.get(url_for('raffles.index')).status_code == 200


def test_get_new(client):
    assert client.get(url_for('raffles.new')).status_code == 200


def test_post_new_no_params(client):
    assert client.post(url_for('raffles.new')).status_code == 422


def test_post_new_invalid_params(client):
    res = client.post(url_for('raffles.new'), data=_invalid_form_params())
    assert res.status_code == 422


def test_post_new_valid_params(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: True)
    monkeypatch.setattr(raffle, 'queue', _stub_raffle_job)
    res = client.post(url_for('raffles.new'), data=_valid_form_params())
    assert res.status_code == 302


def test_raffle_status_missing_job(client):
    res = client.get(url_for('raffles.status', job_id='123abc'))
    assert res.status_code == 404


def test_raffle_status(client, monkeypatch):
    monkeypatch.setattr(Queue, 'fetch_job', lambda self, x: True)
    res = client.get(url_for('raffles.status', job_id='123abc'))
    assert res.status_code == 200


def test_show_missing_raffle(client, db_session):
    res = client.get(url_for('raffles.show', submission_id='123abc'))
    assert res.status_code == 404


def test_show(client, raffle):
    res = client.get(url_for('raffles.show', submission_id='test_id'))
    assert res.status_code == 200


def _stub_raffle_job(raffle_params, user, job_id):
    return [raffle_params, user, job_id]


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
