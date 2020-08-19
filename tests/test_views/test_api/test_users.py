from flask import url_for
import pytest

from tests.factories import RaffleFactory


@pytest.fixture
def raffle():
    return RaffleFactory()


class TestGetUserSubmissions:
    def test_user_has_no_submissions(self, client, mocker):
        mocker.patch("app.db.models.user.User.find_by_jwt", lambda x: mocker.Mock())
        mocker.patch(
            "app.services.reddit_service.get_submissions_for_user", lambda x: []
        )
        mocker.patch("app.util.jwt_helper.decode")

        with client.session_transaction() as session:
            session["jwt"] = "somejwt"
            session["reddit_username"] = "some_username"

        res = client.get(url_for("api.get_user_submissions"))
        assert res.status_code == 200
        assert res.get_json() == []

    def test_user_has_submissions(self):
        pass


class TestGetUserRaffles:
    def test_get_user_raffles_invalid_user(self, client, db_session):
        res = client.get(url_for("api.get_user_raffles", username="invalid123"))
        assert res.status_code == 404

    def test_get_user_raffles_valid_user(self, client, db_session, raffle):
        user = raffle.creator
        res = client.get(url_for("api.get_user_raffles", username=user.username))
        assert res.status_code == 200
        assert len(res.json) == len(user.raffles)
        assert res.json[-1]["submission_id"] == user.raffles[-1].submission_id
