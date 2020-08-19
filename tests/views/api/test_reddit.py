from flask import url_for
import pytest

from tests.factories import RaffleFactory

get_submission_by_url_path = "app.services.reddit_service.get_submission_by_url"


@pytest.fixture
def unverified_raffle():
    return RaffleFactory(unverified=True)


class TestGetRedditSubmission:
    def test_no_params(self, authed_client):
        res = authed_client.get(url_for("api.get_reddit_submission"))
        assert res.status_code == 400

    def test_invalid_submission(self, authed_client, mocker):
        mocker.patch(get_submission_by_url_path).return_value = None
        res = authed_client.get(url_for("api.get_reddit_submission", url="some_url"))
        assert res.status_code == 404

    def test_is_existing_raffle(self, authed_client, mocker, unverified_raffle):
        mocker.patch(get_submission_by_url_path).return_value = {
            "id": unverified_raffle.submission_id
        }

        res = authed_client.get(url_for("api.get_reddit_submission", url="some_url"))
        assert res.status_code == 303

    def test_valid_submission(self, authed_client, mocker):
        mocker.patch(get_submission_by_url_path).return_value = {"id": "1a2b3c"}
        res = authed_client.get(url_for("api.get_reddit_submission", url="some_url"))
        assert res.status_code == 200
