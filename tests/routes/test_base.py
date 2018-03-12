from flask import url_for


def test_index(client):
    assert client.get(url_for('base.index')).status_code == 200


def test_tos(client):
    assert client.get(url_for('base.tos')).status_code == 200


def test_privacy_policy(client):
    assert client.get(url_for('base.privacy_policy')).status_code == 200
