from flask import url_for
from app.views.oauth import (
    MISSING_AUTH_CODE_MESSAGE,
    FAILED_AUTH_CODE_AUTHORIZATION_MESSAGE,
)
import pytest


class TestGetRedditOauthUrl:
    @pytest.fixture
    def get_oauth_url(self, mocker):
        get_oauth_url_mock = mocker.patch("app.services.reddit_service.get_oauth_url")
        get_oauth_url_mock.return_value = "MY_TEST_OAUTH_URL"
        yield get_oauth_url_mock

    def test_returns_oauth_url(self, client, get_oauth_url):
        res = client.get(url_for("oauth.get_reddit_oauth_url"))
        assert res.json.get("reddit_oauth_url") == "MY_TEST_OAUTH_URL"


class TestAuthorizeOauthCode:
    class TestPayloadValidation:
        def test_requires_payload(self, client):
            res = client.post(url_for("oauth.authorize_oauth_code"), json={})
            assert res.status_code == 400
            assert res.get_json().get("error_message") == MISSING_AUTH_CODE_MESSAGE

        def test_requires_auth_code(self, client):
            res = client.post(url_for("oauth.authorize_oauth_code"), json={})
            assert res.status_code == 400
            assert res.get_json().get("error_message") == MISSING_AUTH_CODE_MESSAGE

    class TestCodeAuthorization:
        @pytest.fixture
        def working_authorize(self, mocker):
            authorize = mocker.patch("app.views.oauth.reddit_service.authorize")
            yield authorize

        @pytest.fixture
        def broken_authorize(self, mocker):
            authorize = mocker.patch("app.views.oauth.reddit_service.authorize")
            authorize.side_effect = Exception("lolwut")
            yield authorize

        def test_raises_on_authorization_failure(self, client, broken_authorize):
            res = client.post(
                url_for("oauth.authorize_oauth_code"), json={"code": "MyAuthCode"}
            )
            assert res.status_code == 422
            assert (
                res.get_json().get("error_message")
                == FAILED_AUTH_CODE_AUTHORIZATION_MESSAGE
            )

        def test_returns_jwt_on_success(self, client, working_authorize, mocker):
            mocker.patch("app.views.oauth.reddit_service.get_user_from_token")
            user_instance = mocker.Mock()
            user_instance.get_jwt.return_value = "some jwt"
            mocker.patch(
                "app.views.oauth.User.find_or_create"
            ).return_value = user_instance

            res = client.post(
                url_for("oauth.authorize_oauth_code"), json={"code": "MyAuthCode"}
            )
            assert res.status_code == 200
            assert res.get_json().get("jwt") == "some jwt"
