from flask import url_for
from app.util import reddit
from app.util.raffle_form_validator import RaffleFormValidator
from app.jobs.raffle_job import raffle


class TestSubmissions:
    def test_unauthorized_with_no_login(self, client):
        res = client.get(url_for("api.submissions"))
        assert res.status_code == 401

    def test_unauthorized_when_user_not_found(self, client):
        with client.session_transaction() as session:
            session["jwt"] = "somejwt"

        res = client.get(url_for("api.submissions"))
        assert res.status_code == 401

    def test_successful_fetch(self, client, mocker):
        mocker.patch("app.db.models.User.find_by_jwt", lambda x: mocker.Mock())
        mocker.patch(
            "app.services.reddit_service.get_submissions_for_user", lambda x: []
        )
        mocker.patch("app.util.JwtHelper.decode")

        with client.session_transaction() as session:
            session["jwt"] = "somejwt"
            session["reddit_username"] = "some_username"

        res = client.get(url_for("api.submissions"))
        assert res.status_code == 200
        assert res.get_json() == []


def test_submission_no_params(client):
    res = client.get(url_for("api.submission"))
    assert res.status_code == 400


def test_submission_invalid_submission(client, monkeypatch, db_session):
    monkeypatch.setattr(reddit, "submission_id_from_url", lambda x: None)
    monkeypatch.setattr(reddit, "get_submission", lambda sub_url: None)
    res = client.get(url_for("api.submission", url="some_url"))
    assert res.status_code == 404


def test_submission_existing_raffle(client, monkeypatch, db_session, raffle):
    monkeypatch.setattr(reddit, "submission_id_from_url", lambda x: "test_id")
    monkeypatch.setattr(reddit, "get_submission", lambda sub_url: None)
    res = client.get(url_for("api.submission", url="some_url"))
    assert res.status_code == 303


def test_submission_valid_submission(client, monkeypatch, db_session):
    monkeypatch.setattr(reddit, "submission_id_from_url", lambda x: None)
    monkeypatch.setattr(reddit, "get_submission", lambda sub_url: "something")
    res = client.get(url_for("api.submission", url="some_url"))
    assert res.status_code == 200


def test_post_new_raffle_no_params(client):
    assert client.post(url_for("api.new_raffle")).status_code == 422


def test_post_new_raffle_invalid_params(client):
    res = client.post(url_for("api.new_raffle"), data=_invalid_form_params())
    assert res.status_code == 422


def test_post_new_raffle_valid_params(client, monkeypatch):
    monkeypatch.setattr(RaffleFormValidator, "run", lambda x: True)
    monkeypatch.setattr(raffle, "queue", _stub_raffle_job)
    res = client.post(url_for("api.new_raffle"), data=_valid_form_params())
    assert res.status_code == 202


def test_get_user_raffles_invalid_user(client, db_session):
    res = client.get(url_for("api.get_user_raffles", username="invalid123"))
    assert res.status_code == 404


def test_get_user_raffles_valid_user(client, db_session, user, raffle):
    res = client.get(url_for("api.get_user_raffles", username=user.username))
    assert res.status_code == 200
    assert len(res.json) == len(user.raffles)
    assert res.json[-1]["submission_id"] == user.raffles[-1].submission_id


def _valid_form_params():
    return {
        "submissionUrl": "https://redd.it/57xvjb",
        "winnerCount": 1,
        "minAge": 0,
        "minComment": 0,
        "minLink": 0,
        "ignoredUsers": "[]",
    }


def _invalid_form_params():
    return _valid_form_params().update({"winnerCount": 0})


def _stub_raffle_job(raffle_params, user, job_id):
    return [raffle_params, user, job_id]
