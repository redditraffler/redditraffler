from flask import url_for
import pytest

from tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


def test_show_valid_user(client, user):
    """ Assert that the user's profile page is shown. """
    res = client.get(url_for("users.show", username=user.username))
    assert res.status_code == 200


def test_show_invalid_user(client):
    res = client.get(url_for("users.show", username="someUnknownUser"))
    assert res.status_code == 404
