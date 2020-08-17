from flask import url_for


def test_index(client):
    assert client.get(url_for("base.index")).status_code == 200


def test_about(client):
    assert client.get(url_for("base.about")).status_code == 200


def test_faq(client):
    assert client.get(url_for("base.faq")).status_code == 200


def test_tos(client):
    assert client.get(url_for("base.tos")).status_code == 200


def test_privacy_policy(client):
    assert client.get(url_for("base.privacy_policy")).status_code == 200
