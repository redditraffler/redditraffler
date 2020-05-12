import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app.db.models.raffle import Raffle
from tests.helpers import scoped_session


class RaffleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Raffle
        sqlalchemy_session = scoped_session

    id = factory.Sequence(lambda n: n)
    creator = factory.SubFactory("tests.factories.user_factory.UserFactory")

    submission_id = factory.Faker("pystr", max_chars=10)
    submission_title = factory.Faker("sentence")
    submission_author = factory.Sequence(lambda n: f"RedditAuthor{n}")
    subreddit = factory.LazyFunction(lambda: f"/r/{Faker().word()}")
    winner_count = factory.Faker("pyint", min_value=1, max_value=50)
    min_account_age = factory.Faker("pyint", max_value=1000)
    min_comment_karma = factory.Faker("pyint", max_value=1000)
    min_link_karma = factory.Faker("pyint", max_value=1000)
    min_combined_karma = None
    ignored_users = None

    class Params:
        uses_combined_karma = factory.Trait(
            min_comment_karma=None,
            min_link_karma=None,
            min_combined_karma=factory.Faker("pyint", max_value=1000),
        )

        unverified = factory.Trait(creator=None)
