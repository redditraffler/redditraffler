from app.db.models.raffle import Raffle
from tests.factories import RaffleFactory


class TestRaffle:
    class TestGetVanityMetrics:
        def test_returns_correct_metrics(self, db_session):
            RaffleFactory.create_batch(2)
            RaffleFactory.create_batch(4, subreddit="/r/topsubreddit")
            RaffleFactory.create_batch(3, subreddit="/r/top2subreddit")
            RaffleFactory.create_batch(2, subreddit="/r/top3subreddit")

            result = Raffle.get_vanity_metrics()

            assert (
                result["num_total_verified_raffles"]
                == 2 + 4 + 3 + 2  # Based on counts above
            )
            num_winners_in_db = db_session.execute(
                "select count(*) from winner"
            ).first()[0]
            assert result["num_total_winners"] == num_winners_in_db
            assert result["top_recent_subreddits"] == [
                {"subreddit": "/r/topsubreddit", "num_raffles": 4},
                {"subreddit": "/r/top2subreddit", "num_raffles": 3},
                {"subreddit": "/r/top3subreddit", "num_raffles": 2},
            ]

