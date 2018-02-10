import praw
import app.config as config

SETTINGS = {
    'client_id': config.REDDIT_CLIENT_ID,
    'client_secret': config.REDDIT_CLIENT_SECRET,
    'user_agent': config.REDDIT_USER_AGENT,
    'redirect_uri': config.REDDIT_REDIRECT_URI
}


def get_auth_url():
    r = praw.Reddit(**SETTINGS)
    return r.auth.url(config.REDDIT_AUTH_SCOPES, 'authorized', 'permanent')


def authorize(code):
    r = praw.Reddit(**SETTINGS)
    return r.auth.authorize(code)


def get_username(refresh_token):
    """ Return the Reddit username associated with the given refresh token. """
    r = praw.Reddit(**SETTINGS, refresh_token=refresh_token)
    return r.user.me().name

