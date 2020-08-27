from typing import List
from sqlalchemy import inspect, func
from datetime import datetime, timedelta

from app.extensions import db


class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    submission_id = db.Column(db.Text, index=True, unique=True, nullable=False)
    submission_title = db.Column(db.Text, nullable=False)
    submission_author = db.Column(db.Text, nullable=False)
    subreddit = db.Column(db.Text, nullable=False)
    winner_count = db.Column(db.Integer, nullable=False)
    min_account_age = db.Column(db.Integer, nullable=False)
    min_comment_karma = db.Column(db.Integer, nullable=True)
    min_link_karma = db.Column(db.Integer, nullable=True)
    min_combined_karma = db.Column(db.Integer, nullable=True)
    ignored_users = db.Column(db.Text, nullable=True)

    winners = db.relationship(
        "Winner", backref="raffle", lazy=True, cascade="all, delete-orphan"
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)

    def __repr__(self):
        return "<Raffle {}>".format(self.submission_id)

    @classmethod
    def get_verified_raffles(cls):
        return cls.query.filter(cls.user_id.isnot(None)).all()

    @classmethod
    def get_vanity_metrics(cls) -> dict:
        result = (
            cls.query.with_entities(cls.subreddit, cls.winner_count, cls.created_at)
            .filter(cls.user_id.isnot(None))
            .order_by(cls.created_at.desc())
        ).all()

        # Basic Raffle and Winner stats
        num_total_verified_raffles = len(result)
        num_total_winners = sum([raffle.winner_count for raffle in result])
        num_total_subreddits = len(set([raffle.subreddit for raffle in result]))

        # Get the top 3 subreddits with the most raffles in the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        num_raffles_by_subreddit = (
            cls.query.with_entities(cls.subreddit, func.count())
            .filter(cls.created_at > thirty_days_ago)
            .group_by(cls.subreddit)
            .order_by(func.count().desc())
            .all()
        )
        top_recent_subreddits = [
            {"subreddit": subreddit, "num_raffles": num_raffles}
            for subreddit, num_raffles in num_raffles_by_subreddit
        ]  # Reshape the tuples from the db call into a named dict
        num_recent_subreddits_to_show = min(
            len(top_recent_subreddits), 3
        )  # Possible that we have raffles for fewer than 3 subreddits
        top_recent_subreddits = top_recent_subreddits[:num_recent_subreddits_to_show]

        return {
            "num_total_verified_raffles": num_total_verified_raffles,
            "num_total_winners": num_total_winners,
            "num_total_subreddits": num_total_subreddits,
            "top_recent_subreddits": top_recent_subreddits,
        }

    @classmethod
    def get_recent_raffles(
        cls, include_unverified=False, oldest_raffle_age_days=30
    ) -> List["Raffle"]:
        """Returns a list of raffles that were created no earlier than
        oldest_raffle_age_days ago. Use include_unverified to filter
        unverified raffles from the result set.

        Returns:
            List[Raffle]: The raffles meeting the given criteria
        """
        oldest_raffle_age_days_ago = datetime.now() - timedelta(
            days=oldest_raffle_age_days
        )

        return (
            cls.query.filter(
                cls.created_at > oldest_raffle_age_days_ago,
                True if include_unverified else cls.user_id.isnot(None),
            )
            .order_by(cls.created_at.desc())
            .all()
        )

    def is_verified(self):
        return self.creator and (self.submission_author == self.creator.username)

    def created_at_readable(self):
        return (
            self.created_at.strftime("%B %-d %Y, %-I:%M%p")
            .replace("AM", "am")
            .replace("PM", "pm")
        )

    def as_dict(self):
        exclude = set(["id", "updated_at"])
        res = {}
        for col in inspect(self).mapper.column_attrs:
            if col.key == "created_at":
                res[col.key] = getattr(self, col.key).timestamp()
            elif col.key not in exclude:
                res[col.key] = getattr(self, col.key)
        res["created_at_readable"] = self.created_at_readable()
        return res

    def ignored_users_list(self):
        return self.ignored_users.split(",")

