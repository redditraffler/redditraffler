from datetime import datetime
from flask import current_app

from app.util import CryptoHelper, JwtHelper
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

    def set_refresh_token(self, refresh_token):
        """
        Given a raw Reddit refresh token, encrypts and saves it for this user.

        Args:
            refresh_token (string): Reddit refresh token
        """
        if not refresh_token:
            raise ValueError("Refresh token cannot be empty")

        encrypted_token_bytes = CryptoHelper.encrypt(refresh_token)
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

        return CryptoHelper.decrypt(self.refresh_token_enc).decode()

    def get_jwt(self):
        """
        Returns a JWT containing the user ID and the username.

        Returns:
            bytes: Payload encoded as a JWT bytestring
        """
        payload = {"user_id": self.id, "username": self.username}
        return JwtHelper.encode(payload)
