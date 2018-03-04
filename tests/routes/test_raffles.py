from flask import url_for, request
from app.util import reddit


def test_get_create(client):
    assert client.get(url_for('raffles.create')).status_code == 200


def test_post_create_no_params(client):
    assert client.post(url_for('raffles.create')).status_code == 422


def test_post_create_invalid_params(client):
    res = client.post(url_for('raffles.create'), data=_invalid_form_params())
    assert res.status_code == 422


def test_post_create_valid_params(client, monkeypatch):
    monkeypatch.setattr(reddit, 'get_submission', lambda sub_url: True)
    res = client.post(url_for('raffles.create'), data=_valid_form_params())
    assert res.status_code == 200


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
