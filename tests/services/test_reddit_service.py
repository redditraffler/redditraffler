import pytest


@pytest.fixture(autouse=True)
def praw_reddit(self, mocker):
    praw_reddit_mock = mocker.patch("praw.Reddit")
    praw_reddit_mock.return_value = "Authed Instance"
    yield praw_reddit_mock


class TestRedditService:
    pass
