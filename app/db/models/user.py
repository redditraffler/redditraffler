from datetime import datetime
from flask import current_app

from app.util import crypto_helper, jwt_helper
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
    def find_by_jwt(cls, jwt):
        """
        Given a JWT, queries the database using the user_id in the decoded JWT payload

        Args:
            jwt (obj): The user's JWT

        Returns:
            User: The user identified by the JWT
        """
        user_id = jwt_helper.decode(jwt)["user_id"]
        return cls.query.get(user_id)

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

    def set_refresh_token(self, refresh_token):
        """
        Given a raw Reddit refresh token, encrypts and saves it for this user.

        Args:
            refresh_token (string): Reddit refresh token
        """
        if not refresh_token:
            raise ValueError("Refresh token cannot be empty")

        encrypted_token_bytes = crypto_helper.encrypt(refresh_token)
        self.refresh_token_enc = encrypted_token_bytes
        db.session.add(self)
        db.session.commit()

    def get_refresh_token(self):
        """
        Returns the user's refresh token as a decrypted string.

        Raises:
            AttributeError: When the user doesn't have a saved refresh token

        Returns:
            str: The decrypted refresh token
        """
        if not self.refresh_token_enc:
            raise AttributeError("User does not have a saved refresh token")

        return crypto_helper.decrypt(self.refresh_token_enc).decode()

    def get_jwt(self):
        """
        Returns a JWT containing the user ID and the username.

        Returns:
            str: Payload encoded as a JWT string
        """
        payload = {"user_id": self.id, "username": self.username}
        jwt_bytes = jwt_helper.encode(payload)
        return jwt_bytes.decode()

    def get_profile(self):
        raffles = self.raffles
        raffle_submission_ids = [raf.submission_id for raf in raffles]

        # Vanity stats
        raffle_count = len(self.raffles)
        num_winners_selected = sum([raf.winner_count for raf in raffles])

        return dict(
            created_at=self.created_at.isoformat(),
            raffle_submission_ids=raffle_submission_ids,
            raffle_count=raffle_count,
            num_winners_selected=num_winners_selected,
        )
