from sqlalchemy import orm

scoped_session = orm.scoped_session(orm.sessionmaker())


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
