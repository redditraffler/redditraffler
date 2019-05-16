from app.util import reddit
from app.util.raffler import Raffler
from app.jobs.raffle_job import raffle
from app.db.models import Raffle, User
from tests.helpers import raffler_params
import pytest


@pytest.fixture(autouse=True)
def patch_raffler_class(monkeypatch):
    monkeypatch.setattr(Raffler, "__init__", _stub_raffler_init)
    monkeypatch.setattr(Raffler, "fetch_comments", lambda x: True)
    monkeypatch.setattr(Raffler, "select_winners", lambda x: True)
    monkeypatch.setattr(Raffler, "get_serialized_winners", _stub_winners)
    monkeypatch.setattr(reddit, "get_submission", _stub_submission)
    yield


class TestRaffle:
    class TestSuccessfulRaffle:
        def test_raffle_guest_db_saving(self, db_session, client):
            job = raffle.queue(raffler_params(), None)

            saved_raffle = Raffle.query.filter_by(submission_id="abc123").first()
            assert saved_raffle
            assert not saved_raffle.creator
            assert len(saved_raffle.winners) == 1
            assert saved_raffle.winners[0].username == "test-user"

        def test_raffle_verified_db_saving(self, db_session, client):
            user = User(username="verified_redditor")
            db_session.add(user)
            db_session.commit()
            job = raffle.queue(raffler_params(), user)

            saved_raffle = Raffle.query.filter_by(submission_id="abc123").first()
            assert saved_raffle
            assert saved_raffle.creator.username == "verified_redditor"
            assert len(saved_raffle.winners) == 1
            assert saved_raffle.winners[0].username == "test-user"

    class TestFailure:
        @pytest.fixture
        def job(self, mocker):
            job = mocker.Mock()
            job.meta = {}
            job.save_meta = mocker.Mock()
            yield job

        @pytest.fixture
        def get_current_job(self, mocker, job):
            get_current_job = mocker.patch("app.jobs.raffle_job.get_current_job")
            get_current_job.return_value = job
            yield get_current_job

        @pytest.fixture
        def reddit(self, mocker):
            reddit = mocker.patch("app.jobs.raffle_job.reddit")
            reddit.submission_id_from_url = mocker.Mock()
            reddit.get_submission = mocker.Mock(return_value=_stub_submission(""))
            yield reddit

        @pytest.fixture
        def raffler(self, mocker):
            raffler = mocker.patch("app.jobs.raffle_job.Raffler")
            raffler.return_value = mocker.Mock()
            raffler.return_value.fetch_comments = mocker.Mock(
                side_effect=ValueError("Some Random Error")
            )
            yield raffler

        def test_set_error_message_to_job(
            self, mocker, reddit, raffler, job, get_current_job
        ):
            raffle.queue(raffler_params(), None)
            assert job.meta.get("status") == "Error: Some Random Error"
            assert job.meta.get("error") == True


def _stub_raffler_init(
    self,
    submission_url,
    winner_count,
    min_account_age,
    min_comment_karma,
    min_link_karma,
    min_combined_karma,
    ignored_users,
):
    return None


def _stub_winners(self):
    return [
        {
            "user": {
                "username": "test-user",
                "age": 100,
                "comment_karma": 100,
                "link_karma": 100,
            },
            "comment_url": "https://redd.it/comments/abc123",
        }
    ]


def _stub_submission(sub_url):
    return {
        "id": "abc123",
        "author": "test_user",
        "title": "test_title",
        "url": "https://redd.it/abc123",
        "subreddit": "test",
        "created_at_utc": 1520193497,
    }


def _raffle_params():
    return {
        "submission_url": "https://redd.it/57xvjb",
        "winner_count": 1,
        "min_account_age": 0,
        "min_comment_karma": 0,
        "min_link_karma": 0,
    }


def _submission():
    return {
        "id": "57xvjb",
        "author": "xozzo",
        "title": "pyfootball - A Python API wrapper for football-data.org, \
                  an open source football (soccer) data REST API",
        "url": "https://www.reddit.com/r/coolgithubprojects/comments/57xv \
                jb/pyfootball_a_python_api_wrapper_for/",
        "subreddit": "coolgithubprojects",
        "created_at_utc": 1476717718.0,
    }
