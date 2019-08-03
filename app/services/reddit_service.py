import praw
import functools

from praw.models import Submission


def with_reddit_instance(fnToWrap):
    """ Injects a praw.Reddit instance, created using the RedditService instance's
    settings, as a parameter to the wrapped function. If the refresh_token keyword
    argument is present, an authenticated instance will be provided. """

    @functools.wraps(fnToWrap)
    def reddit_instance_injector(*args, **kwargs):
        reddit_service_instance = args[0]
        refresh_token = kwargs.get("refresh_token")

        if refresh_token is not None:
            return fnToWrap(
                *args,
                **kwargs,
                reddit=praw.Reddit(
                    **reddit_service_instance.settings, refresh_token=refresh_token
                ),
            )
        else:
            return fnToWrap(*args, **kwargs, reddit=reddit_service_instance._reddit)

    return reddit_instance_injector


class RedditService:
    def init_app(self, app):
        self.settings = {
            "client_id": app.config["REDDIT_CLIENT_ID"],
            "client_secret": app.config["REDDIT_CLIENT_SECRET"],
            "user_agent": app.config["REDDIT_USER_AGENT"],
            "redirect_uri": app.config["REDDIT_REDIRECT_URI"],
        }
        self.auth_scopes = app.config["REDDIT_AUTH_SCOPES"]
        self._reddit = praw.Reddit(**self.settings)

    @with_reddit_instance
    def get_oauth_url(self, reddit):
        """ Returns the URL that directs the user to Reddit's OAuth page. """
        return reddit.auth.url(self.auth_scopes, "auth", "permanent")

    @with_reddit_instance
    def authorize(self, reddit, code):
        """ Given a valid code from Reddit's OAuth redirect, returns a refresh token for the user. """
        return reddit.auth.authorize(code)

    @with_reddit_instance
    def get_user_from_token(self, reddit, refresh_token=None):
        """ Returns the authorized Redditor. """
        return reddit.user.me()

    @with_reddit_instance
    def get_submissions_for_user(self, reddit, refresh_token=None):
        """ Returns the submissions for the authorized Redditor. """
        submissions = reddit.user.me().submissions.new()
        return [_extract_submission_info(s) for s in submissions]

    @with_reddit_instance
    def get_submission_by_url(self, reddit, url):
        try:
            submission_id = Submission.id_from_url(url)
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
