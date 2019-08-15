import praw
import prawcore

from praw.models import Submission


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

    def get_oauth_url(self):
        """ Returns the URL that directs the user to Reddit's OAuth page. """
        return self._reddit.auth.url(self.auth_scopes, "auth", "permanent")

    def authorize(self, code):
        """ Given a valid code from Reddit's OAuth redirect, returns a refresh token \
            for the user. """
        return self._reddit.auth.authorize(code)

    def get_user_from_token(self, refresh_token):
        """ Returns the authorized Redditor. """
        return praw.Reddit(**self.settings, refresh_token=refresh_token).user.me()

    def get_submissions_for_user(self, refresh_token):
        """ Returns the submissions for the authorized Redditor. """
        submissions = (
            praw.Reddit(**self.settings, refresh_token=refresh_token)
            .user.me()
            .submissions.new()
        )
        return [_extract_submission_info(s) for s in submissions]

    def get_submission_by_url(self, url):
        try:
            submission_id = Submission.id_from_url(url)
            submission = self._reddit.submission(submission_id)
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
