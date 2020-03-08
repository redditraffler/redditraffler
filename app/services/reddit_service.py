import praw
import prawcore

from flask import current_app

_reddit = None
_auth_scopes = None


def _get_reddit_instance(refresh_token=None):
    """
    Returns an authenticated instance of praw.Reddit if a refresh_token is provided.
    Otherwise, returns a cached praw.Reddit instance or initializes it.

    Args:
        refresh_token ([str], optional): Reddit refresh token. Defaults to None.

    Returns:
        [praw.Reddit]: A praw.Reddit instance
    """

    global _reddit
    global _auth_scopes

    _auth_scopes = current_app.config["REDDIT_AUTH_SCOPES"]
    settings = {
        "client_id": current_app.config["REDDIT_CLIENT_ID"],
        "client_secret": current_app.config["REDDIT_CLIENT_SECRET"],
        "user_agent": current_app.config["REDDIT_USER_AGENT"],
        "redirect_uri": current_app.config["REDDIT_REDIRECT_URI"],
    }

    if refresh_token is not None:
        return praw.Reddit(**settings, refresh_token=refresh_token)

    if _reddit is not None:
        return _reddit

    _reddit = praw.Reddit(**settings)
    return _reddit


def get_oauth_url():
    """ Returns the URL that directs the user to Reddit's OAuth page. """
    reddit = _get_reddit_instance()
    return reddit.auth.url(_auth_scopes, "auth", "permanent")


def authorize(code):
    """ Given a valid code from Reddit's OAuth redirect, returns a refresh token \
        for the user. """
    reddit = _get_reddit_instance()
    return reddit.auth.authorize(code)


def get_user_from_token(refresh_token):
    """ Returns the authorized Redditor. """
    return _get_reddit_instance(refresh_token).user.me()


def get_submissions_for_user(refresh_token):
    """ Returns the submissions for the authorized Redditor. """
    authed_reddit = _get_reddit_instance(refresh_token)
    submissions = authed_reddit.user.me().submissions.new()
    return [_extract_submission_info(s) for s in submissions]


def get_submission_by_url(url):
    reddit = _get_reddit_instance()
    try:
        submission_id = praw.models.Submission.id_from_url(url)
        submission = reddit.submission(submission_id)
        return _extract_submission_info(submission)
    except (prawcore.exceptions.NotFound, praw.exceptions.ClientException):
        return None


def _extract_submission_info(submission):
    return {
        "id": submission.id,
        "author": submission.author.name if submission.author else None,
        "title": submission.title,
        "url": f"https://www.reddit.com{submission.permalink}",
        "subreddit": submission.subreddit.display_name,
        "created_at_utc": submission.created_utc,
    }
