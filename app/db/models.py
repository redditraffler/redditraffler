from app.extensions import db
from datetime import datetime
from sqlalchemy import inspect


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)

    raffles = db.relationship('Raffle', backref='creator', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    submission_id = db.Column(db.String(64), index=True, unique=True)
    submission_title = db.Column(db.String(128))
    submission_author = db.Column(db.String(64))
    subreddit = db.Column(db.String(64))
    winner_count = db.Column(db.Integer)
    min_account_age = db.Column(db.Integer)
    min_comment_karma = db.Column(db.Integer)
    min_link_karma = db.Column(db.Integer)

    winners = db.relationship('Winner',
                              backref='raffle',
                              lazy=True,
                              cascade='all, delete-orphan')
    ignored_users = db.relationship('IgnoredUser',
                                    backref='raffle',
                                    lazy=True,
                                    cascade='all, delete-orphan')

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=True,
                        index=True)

    def __repr__(self):
        return '<Raffle {}>'.format(self.submission_id)

    def is_verified(self):
        return self.creator and \
               (self.submission_author == self.creator.username)

    def created_at_readable(self):
        return self.created_at.strftime('%B %-d %Y, %-I:%M%p') \
                              .replace('AM', 'am') \
                              .replace('PM', 'pm')

    def as_dict(self):
        exclude = set(['id', 'created_at', 'updated_at'])
        res = {}
        for col in inspect(self).mapper.column_attrs:
            if col.key not in exclude:
                res[col.key] = getattr(self, col.key)
        return res


class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    username = db.Column(db.String(64))
    account_age = db.Column(db.Integer)
    comment_karma = db.Column(db.Integer)
    link_karma = db.Column(db.Integer)
    comment_url = db.Column(db.String(128))

    raffle_id = db.Column(db.Integer,
                          db.ForeignKey('raffle.id'),
                          nullable=False,
                          index=True)


class IgnoredUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    username = db.Column(db.String(64))

    raffle_id = db.Column(db.Integer,
                          db.ForeignKey('raffle.id'),
                          nullable=False,
                          index=True)
