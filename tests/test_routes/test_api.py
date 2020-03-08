from flask import url_for

get_submission_by_url_path = "app.services.reddit_service.get_submission_by_url"


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
        mocker.patch("app.db.models.user.User.find_by_jwt", lambda x: mocker.Mock())
        mocker.patch(
            "app.services.reddit_service.get_submissions_for_user", lambda x: []
        )
        mocker.patch("app.util.jwt_helper.decode")

        with client.session_transaction() as session:
            session["jwt"] = "somejwt"
            session["reddit_username"] = "some_username"

        res = client.get(url_for("api.submissions"))
        assert res.status_code == 200
        assert res.get_json() == []


class TestSubmission:
    def test_no_params(self, authed_client):
        res = authed_client.get(url_for("api.submission"))
        assert res.status_code == 400

    def test_invalid_submission(self, authed_client, mocker):
        mocker.patch(get_submission_by_url_path).return_value = None
        res = authed_client.get(url_for("api.submission", url="some_url"))
        assert res.status_code == 404

    def test_is_existing_raffle(self, authed_client, mocker, raffle):
        mocker.patch(get_submission_by_url_path).return_value = {"id": "test_id"}
        res = authed_client.get(url_for("api.submission", url="some_url"))
        assert res.status_code == 303

    def test_valid_submission(self, authed_client, mocker):
        mocker.patch(get_submission_by_url_path).return_value = {"id": "1a2b3c"}
        res = authed_client.get(url_for("api.submission", url="some_url"))
        assert res.status_code == 200


class TestNewRaffle:
    def test_no_params(self, authed_client):
        assert authed_client.post(url_for("api.new_raffle")).status_code == 422

    def test_params_failed_validation(self, authed_client):
        res = authed_client.post(url_for("api.new_raffle"), data=_invalid_form_params())
        assert res.status_code == 422

    def test_valid_params(self, authed_client, mocker):
        mocker.patch(
            "app.util.raffle_form_validator.RaffleFormValidator.run", lambda x: True
        )
        mocker.patch(
            "app.services.reddit_service.get_submission_by_url"
        ).return_value = {"id": "1a2b3c"}
        mocker.patch("app.jobs.raffle_job.raffle.queue")
        res = authed_client.post(url_for("api.new_raffle"), data=_valid_form_params())
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
