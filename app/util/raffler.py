from datetime import datetime
import praw
import app.config as config


class Raffler():
    def __init__(self, submission_url, winner_count, min_age,
                 min_comment_karma, min_link_karma):
        self.reddit = praw.Reddit(client_id=config.BOT_CLIENT_ID,
                                  client_secret=config.BOT_CLIENT_SECRET,
                                  user_agent=config.REDDIT_USER_AGENT,
                                  username=config.BOT_USERNAME,
                                  password=config.BOT_PASSWORD)

        self.submission = self.reddit.submission(url=submission_url)
        self.winner_count = int(winner_count)
        self.min_age = int(min_age)
        self.min_comment_karma = int(min_comment_karma)
        self.min_link_karma = int(min_link_karma)
        self._winners = set()
        self._entries = set()

    def fetch_comments(self):
        self.submission.comment_sort = 'random'
        self.submission.comments.replace_more(limit=20)
        for comment in self.submission.comments.list():
            if self._is_valid_comment(comment):
                self._entries.add(comment)

    def select_winners(self):
        while (len(self._entries)) > 0 and \
              (self.winner_count - len(self._winners) > 0):
            entry = self._entries.pop()
            author = entry.author
            user = User(username=author.name,
                        age=Raffler._account_age_days(author.created_utc),
                        comment_karma=author.comment_karma,
                        link_karma=author.link_karma)

            if self._is_valid_winner(user):
                self._winners.add(user)

        return len(self._winners) == self.winner_count

    def _is_valid_comment(self, comment):
        return (comment.is_root) and \
               (comment.body is not None) and \
               (comment.author is not None) and \
               (comment not in self._entries)

    def _is_valid_winner(self, user):
        return (user.age >= self.min_age) and \
               (user.comment_karma >= self.min_comment_karma) and \
               (user.link_karma >= self.min_link_karma)

    @staticmethod
    def _account_age_days(created_utc):
        return (datetime.utcnow() -
                datetime.utcfromtimestamp(created_utc)).days


class User():
    def __init__(self, username, age, comment_karma, link_karma):
        self.username = username
        self.age = age
        self.comment_karma = comment_karma
        self.link_karma = link_karma
