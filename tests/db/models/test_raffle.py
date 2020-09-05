from datetime import datetime, timedelta, timezone

from app.db.models.raffle import Raffle
from tests.factories import RaffleFactory


class TestRaffle:
    class TestGetVanityMetrics:
        def test_returns_correct_metrics(self, db_session):
            RaffleFactory.create_batch(2)
            RaffleFactory.create_batch(5, subreddit="/r/topsubreddit")
            RaffleFactory.create_batch(4, subreddit="/r/top2subreddit")
            RaffleFactory.create_batch(3, subreddit="/r/top3subreddit")

            result = Raffle.get_vanity_metrics()

            assert (
                result["num_total_verified_raffles"]
                == 2 + 5 + 4 + 3  # Based on counts above
            )
            num_winners_in_db = db_session.execute(
                "select count(*) from winner"
            ).first()[0]
            num_distinct_subreddits_in_db = db_session.execute(
                "select count(distinct subreddit) from raffle"
            ).first()[0]
            assert result["num_total_winners"] == num_winners_in_db
            assert result["num_total_subreddits"] == num_distinct_subreddits_in_db
            assert result["top_recent_subreddits"] == [
                {"subreddit": "/r/topsubreddit", "num_raffles": 5},
                {"subreddit": "/r/top2subreddit", "num_raffles": 4},
                {"subreddit": "/r/top3subreddit", "num_raffles": 3},
            ]

    class TestGetRecentRaffles:
        def test_returns_with_default_params(self):
            RaffleFactory.create(unverified=True)
            RaffleFactory.create(created_at=datetime.now() - timedelta(days=31))
            expected_raffle = RaffleFactory.create()

            result = Raffle.get_recent_raffles()

            assert result == [expected_raffle]

        def test_returns_with_params(self):
            expected_raffle = RaffleFactory.create(
                unverified=True, created_at=(datetime.now() - timedelta(days=59))
            )

            result = Raffle.get_recent_raffles(
                include_unverified=True, oldest_raffle_age_days=60
            )

            assert result == [expected_raffle]

    class TestAsDict:
        def test_returns_expected_fields(self):
            test_timestamp = datetime.now()
            raffle = RaffleFactory.create(
                created_at=test_timestamp,
                submission_id="abc",
                submission_title="hello this &amp; that and y&#39;all gotta see this &lt;&gt;&quot;",
                submission_author="testUser",
                subreddit="somecommunity",
                winner_count=1,
                min_account_age=0,
                min_comment_karma=0,
                min_link_karma=0,
            )

            result = raffle.as_dict()

            assert result == {
                "user_id": None,
                "created_at": test_timestamp.replace(tzinfo=timezone.utc).timestamp(),
                "created_at_readable": raffle.created_at_readable(),
                "submission_id": "abc",
                "submission_title": "hello this & that and y'all gotta see this <>\"",
                "submission_author": "testUser",
                "subreddit": "somecommunity",
                "winner_count": 1,
                "min_account_age": 0,
                "min_comment_karma": 0,
                "min_link_karma": 0,
                "min_combined_karma": None,
                "ignored_users": None,
            }
