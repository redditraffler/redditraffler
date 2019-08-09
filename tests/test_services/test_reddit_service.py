import pytest

from app.services.reddit_service import with_reddit_instance


class TestWithRedditInstance:
    @pytest.fixture
    def praw_reddit(self, mocker):
        praw_reddit_mock = mocker.patch("praw.Reddit")
        praw_reddit_mock.return_value = "Authed Instance"
        yield praw_reddit_mock

    @pytest.fixture(autouse=True)
    def reddit_service(self, mocker):
        # NOTE: In this test, reddit_service takes the place of what would be 'self'
        # when used in a RedditService instance.
        service = mocker.Mock()
        service.settings = {
            "client_id": 123,
            "client_secret": "abc",
            "user_agent": "test",
            "redirect_uri": "localhost:1234",
        }
        service._reddit = mocker.Mock()
        yield service

    def test_without_refresh_token_injects_unauthed_instance(
        self, praw_reddit, reddit_service
    ):
        @with_reddit_instance
        def wrapped_fn(reddit_service, reddit):
            assert reddit == reddit_service._reddit
            assert not praw_reddit.called

        wrapped_fn(reddit_service)

    def test_with_refresh_token_injects_authed_instance(
        self, praw_reddit, reddit_service
    ):
        @with_reddit_instance
        def wrapped_fn(reddit_service, reddit, refresh_token):
            assert refresh_token is not None
            assert praw_reddit.called
            assert reddit == praw_reddit.return_value

        wrapped_fn(reddit_service, refresh_token="Some Random Token")

