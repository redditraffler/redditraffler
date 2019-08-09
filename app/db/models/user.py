from datetime import datetime

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
