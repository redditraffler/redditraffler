import pytest

from flask import url_for, session

from app.db.models.user import User
from tests.factories import UserFactory


class TestLogout:
    def test_clear_session(self, client):
        res = client.post(url_for("auth.logout"))
        assert not session
        assert res.status_code == 302


class TestAuthRedirect:
    TEST_USERNAME = "test_user"

    @pytest.fixture
    def mock_reddit(self, mocker):
        mock_reddit = mocker.patch("app.views.auth.reddit_service")
        mock_reddit.authorize.return_value = "test_token"
        yield mock_reddit

    @pytest.fixture
    def test_user(self):
        return UserFactory(username=self.TEST_USERNAME)

    def test_redirect_when_already_logged_in(self, client):
        with client.session_transaction() as session:
            session["jwt"] = "some_jwt"
            session["reddit_username"] = "test_username"
        res = client.get(url_for("auth.auth_redirect"))
        assert res.status_code == 302

    def test_redirect_when_access_denied(self, client):
        params = {"error": "access_denied"}
        res = client.get(url_for("auth.auth_redirect"), query_string=params)
        assert res.status_code == 302

    def test_valid_token_existing_user(self, client, mocker, mock_reddit, test_user):
        mock_user = mocker.Mock()
        mock_user.name = self.TEST_USERNAME
        mock_reddit.get_user_from_token.return_value = mock_user
        user_count_before_call = User.query.count()

        res = client.get(url_for("auth.auth_redirect"))

        assert User.query.count() == user_count_before_call
        assert "jwt" in session and "reddit_username" in session

        assert res.status_code == 302

    def test_valid_token_new_user(self, client, mocker, mock_reddit):
        mock_user = mocker.Mock()
        mock_user.name = "test_new_user"
        mock_reddit.get_user_from_token.return_value = mock_user
        user_count_before_call = User.query.count()

        res = client.get(url_for("auth.auth_redirect"))

        assert User.query.count() == user_count_before_call + 1
        assert User.query.all()[-1].username == "test_new_user"
        assert "jwt" in session and "reddit_username" in session

        assert res.status_code == 302
