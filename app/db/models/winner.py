from datetime import datetime

from app.extensions import db


class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    username = db.Column(db.Text, nullable=False)
    account_age = db.Column(db.Integer, nullable=False)
    comment_karma = db.Column(db.Integer, nullable=False)
    link_karma = db.Column(db.Integer, nullable=False)
    comment_url = db.Column(db.Text, nullable=False)

    raffle_id = db.Column(
        db.Integer, db.ForeignKey("raffle.id"), nullable=False, index=True
    )
