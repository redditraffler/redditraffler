from flask import url_for


def test_index(client):
    assert client.get(url_for('raffles.create')).status_code == 200
