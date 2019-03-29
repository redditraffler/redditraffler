from app.util.raffler import Raffler
from tests.helpers import raffler_params
import praw


def test_init(mocker):
    mocker.patch("praw.Reddit")
    params = raffler_params()
    r = Raffler(**params)
    assert r.winner_count == params["winner_count"]
    assert r.min_account_age == params["min_account_age"]
    assert r.min_comment_karma == params["min_comment_karma"]
    assert r.min_link_karma == params["min_link_karma"]
    assert isinstance(r._winners, dict)
    assert isinstance(r._entries, set)
