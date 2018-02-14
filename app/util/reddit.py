import praw
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


def _serialize(submission):
    """ Extracts the needed submission data and inserts them in a dict. """
    return {
        'title': submission.title,
        'link': submission.shortlink,
        'subreddit': submission.subreddit.display_name
    }
