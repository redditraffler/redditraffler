from app.db.models import raffle, user, winner
from app.extensions import db


def truncate_db():
    models = [winner.Winner, raffle.Raffle, user.User]  # Specify models with FKs first
    for model in models:
        db.session.query(model).delete()
    db.session.commit()


def raffler_params():
    return {
        "submission_url": "https://redd.it/4re9cx",
        "winner_count": 5,
        "min_account_age": 5,
        "min_combined_karma": None,
        "min_comment_karma": 5,
        "min_link_karma": 5,
        "ignored_users": ["TestUser"],
    }


def raffler_params_combined_karma():
    return {
        "submission_url": "https://redd.it/4re9cx",
        "winner_count": 5,
        "min_account_age": 5,
        "min_combined_karma": 15,
        "min_comment_karma": None,
        "min_link_karma": None,
        "ignored_users": ["TestUser"],
    }
