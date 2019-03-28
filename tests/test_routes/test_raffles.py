from flask import url_for, request
from rq.queue import Queue


def test_index(client, db_session):
    assert client.get(url_for("raffles.index")).status_code == 200


def test_get_new(client):
    assert client.get(url_for("raffles.new")).status_code == 200


def test_raffle_status_missing_job(client):
    res = client.get(url_for("raffles.status", job_id="123abc"))
    assert res.status_code == 404


def test_raffle_status(client, monkeypatch):
    monkeypatch.setattr(Queue, "fetch_job", lambda self, x: True)
    res = client.get(url_for("raffles.status", job_id="123abc"))
    assert res.status_code == 200


def test_show_missing_raffle(client, db_session):
    res = client.get(url_for("raffles.show", submission_id="123abc"))
    assert res.status_code == 404


def test_show(client, raffle):
    res = client.get(url_for("raffles.show", submission_id="test_id"))
    assert res.status_code == 200
