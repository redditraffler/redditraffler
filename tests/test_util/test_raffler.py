from app.util.raffler import Raffler
from tests.helpers import raffler_params, raffler_params_combined_karma
import pytest


@pytest.fixture(autouse=True)
def prawReddit(mocker):
    mocker.patch("app.util.raffler.praw.Reddit")


class TestRaffler:
    class TestInit:
        def test_set_correct_values(self, mocker):
            params = raffler_params()
            r = Raffler(**params)
            assert r.winner_count == params["winner_count"]
            assert r.min_account_age == params["min_account_age"]
            assert r.min_comment_karma == params["min_comment_karma"]
            assert r.min_combined_karma == None
            assert r.min_link_karma == params["min_link_karma"]
            assert isinstance(r._winners, dict)
            assert isinstance(r._entries, set)

    class TestUserHasSufficientKarma:
        @pytest.fixture
        def winner(self, mocker):
            yield mocker.Mock(comment_karma=15, link_karma=5)

        @pytest.fixture
        def loser(self, mocker):
            yield mocker.Mock(comment_karma=0, link_karma=0)

        class TestMinCombinedKarma:
            def test_user_passes_check(self, winner):
                r = Raffler(**raffler_params_combined_karma())
                assert r._user_has_sufficient_karma(winner) == True

            def test_user_fails_check(self, loser):
                r = Raffler(**raffler_params_combined_karma())
                assert r._user_has_sufficient_karma(loser) == False

        class TestMinCommentAndLinkKarma:
            def test_user_passes_check(self, winner):
                r = Raffler(**raffler_params())
                assert r._user_has_sufficient_karma(winner) == True

            def test_user_fails_check(self, loser):
                r = Raffler(**raffler_params())
                assert r._user_has_sufficient_karma(loser) == False
