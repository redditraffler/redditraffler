from flask import url_for
import pytest

from tests.factories import UserFactory


@pytest.fixture
def user():
    user = UserFactory()
    user.get_profile = lambda: {}  # Stub out get_profile()
    return user


class TestGetProfile:
    def test_user_not_found(self, client):
        res = client.get(url_for("api_users.get_profile", username="idk"))
        assert res.status_code == 404

    def test_user_found(self, client, user):
        res = client.get(url_for("api_users.get_profile", username=user.username))

        assert res.status_code == 200
        assert res.json == {}
