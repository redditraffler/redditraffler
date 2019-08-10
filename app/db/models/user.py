from datetime import datetime
from flask import current_app

from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    refresh_token_enc = db.Column(db.LargeBinary, unique=True, nullable=True)

    raffles = db.relationship("Raffle", backref="creator", lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    @classmethod
    def find_or_create(cls, username):
        """
        Given a username, try to find the user by username or create the user if
        it does not exist.

        Args:
            username (str): The username to search or create

        Raises:
            ValueError: When the username is empty or with length < 3

        Returns:
            User: The found or created user
        """
        if not username or len(username) < 3:
            raise ValueError("Username must be non-empty")

        user = cls.query.filter_by(username=username).first()
        if user is not None:
            return user

        new_user = cls(username=username)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("Created new user", {"username": username})
        return new_user
