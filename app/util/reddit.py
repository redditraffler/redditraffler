import praw
import prawcore
import app.config as config

SETTINGS = {
    'client_id': config.REDDIT_CLIENT_ID,
    'client_secret': config.REDDIT_CLIENT_SECRET,
    'user_agent': config.REDDIT_USER_AGENT,
    'redirect_uri': config.REDDIT_REDIRECT_URI
}


def get_auth_url():
    """ Returns the Reddit URL used to obtain permissions from the user. """
    r = praw.Reddit(**SETTINGS)
    return r.auth.url(config.REDDIT_AUTH_SCOPES, 'authorized', 'permanent')


def authorize(code):
    """ Accepts a code from Reddit's auth redirect. Returns a refresh token
        for the user. """
    r = praw.Reddit(**SETTINGS)
    return r.auth.authorize(code)


def get_username(refresh_token):
    """ Return the Reddit username associated with the given refresh token. """
    r = praw.Reddit(**SETTINGS, refresh_token=refresh_token)
    return r.user.me().name


def get_user_submissions(refresh_token):
    """ Return the Redditor's submissions ordered latest to oldest. """
    r = praw.Reddit(**SETTINGS, refresh_token=refresh_token)
    submissions = r.user.me().submissions.new()
    result = [_serialize(s) for s in submissions]
    return result


def get_submission(sub_id=None, sub_url=None):
    """ Returns a serialized submission based on the given ID or URL, or
    None if the ID or URL is invalid. """
    r = praw.Reddit(**SETTINGS)

    if not (sub_id or sub_url):
        return None

    try:
        submission = r.submission(id=sub_id) if sub_id else \
                     r.submission(url=sub_url)
        return _serialize(submission)
    except (prawcore.exceptions.NotFound, praw.exceptions.ClientException):
        return None


def id_from_url(url):
    return praw.models.Submission.id_from_url(url)


def _serialize(submission):
    """ Extracts the needed submission data and inserts them in a dict. """
    REDDIT_BASE_URL = 'https://www.reddit.com'
    return {
        'id': submission.id,
        'author': submission.author.name if submission.author else None,
        'title': submission.title,
        'url': REDDIT_BASE_URL + submission.permalink,
        'subreddit': submission.subreddit.display_name,
        'created_at_utc': submission.created_utc
    }
