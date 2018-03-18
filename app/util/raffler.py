from app.config import BaseConfig as config
from datetime import datetime
import praw
import prawcore


class Raffler():
    def __init__(self, submission_url, winner_count, min_account_age,
                 min_comment_karma, min_link_karma):
        """ Initialize a Reddit instance and helper data structures,
        fetch the submission, and set all raffle parameters. """
        self.reddit = praw.Reddit(client_id=config.BOT_CLIENT_ID,
                                  client_secret=config.BOT_CLIENT_SECRET,
                                  user_agent=config.REDDIT_USER_AGENT,
                                  username=config.BOT_USERNAME,
                                  password=config.BOT_PASSWORD)
        self.submission = self.reddit.submission(url=submission_url)
        self.winner_count = int(winner_count)
        self.min_account_age = int(min_account_age)
        self.min_comment_karma = int(min_comment_karma)
        self.min_link_karma = int(min_link_karma)

        self._winners = {}
        self._entries = set()

    def fetch_comments(self):
        """ Fetch the submission's comments in a random order.
        `replace_more(limit=20)` is equivalent to scrolling down in a
        submission to load more comments. Top-level, valid comments are
        then added to an internal set `_entries`. Returns whether the
        loop succeeded in finding at least as many entries as
        `winner_count`. """
        self.submission.comment_sort = 'random'
        self.submission.comments.replace_more(limit=20)
        for comment in self.submission.comments.list():
            if self._is_valid_comment(comment):
                self._entries.add(comment)

        if len(self._entries) < self.winner_count:
            msg = 'winner_count exceeds valid comments. winner_count: {0}, '\
                  'comments: {1}'.format(self.winner_count, len(self._entries))
            raise ValueError(msg)

    def select_winners(self):
        """ Loop over the internal set of entries to find comments whose
        author meets the criteria set. Authors that meet the criteria are
        added to an internal dict `_winners`. Returns whether the loop
        succeeded in finding enough winners to match `winner_count`.
        """
        while (len(self._entries) > 0) and \
              (len(self._winners) < self.winner_count):
            entry = self._entries.pop()
            user = self._try_create_user(entry.author)
            if user and self._is_valid_winner(user):
                self._winners.update({user: entry})

        if len(self._winners) < self.winner_count:
            msg = 'winner_count exceeds eligible winners. winner_count: {0}, '\
                  'winners: {1}'.format(self.winner_count, len(self._winners))
            raise ValueError(msg)

    def get_serialized_winners(self):
        result = []
        for user, comment in self._winners.items():
            result.append({
                'user': user.as_dict(),
                'comment_url': 'https://reddit.com' + comment.permalink,
            })
        return result

    def _is_valid_comment(self, comment):
        """ Returns true if the comment is in the raffle's submission, and
        it is not banned or removed. """
        # TODO: Find possible exceptions raised
        try:
            return (comment.is_root) and \
                   (comment.body is not None) and \
                   (comment.author is not None) and \
                   (comment not in self._entries)
        except:
            current_app.logger.exception('Exception in _is_valid_comment')
            return False

    def _is_valid_winner(self, user):
        """ Returns true if the user meets the raffle requirements and it
        the user only has one comment in the raffle submission. """
        # TODO: Find possible exceptions raised
        try:
            return (user.age >= self.min_account_age) and \
                   (user.comment_karma >= self.min_comment_karma) and \
                   (user.link_karma >= self.min_link_karma)
        except:
            current_app.logger.exception('Exception in _is_valid_winner')
            return False

    def _try_create_user(self, author):
        """ Utility function to make sure the author of an entry isn't banned
        or anything along those lines. """
        try:
            user = self.User(username=author.name,
                             age=Raffler._account_age_days(author.created_utc),
                             comment_karma=author.comment_karma,
                             link_karma=author.link_karma)
            return user
        except (prawcore.exceptions.NotFound, AttributeError):
            return None

    @staticmethod
    def _account_age_days(created_utc):
        """ Utility function to get account age in days. """
        return (datetime.utcnow() -
                datetime.utcfromtimestamp(created_utc)).days

    class User():
        def __init__(self, username, age, comment_karma, link_karma):
            self.username = username
            self.age = age
            self.comment_karma = comment_karma
            self.link_karma = link_karma

        def __hash__(self):
            return hash(self.username)

        def __eq__(self, other):
            return self.username == other.username

        def as_dict(self):
            return {
                'username': self.username,
                'age': self.age,
                'comment_karma': self.comment_karma,
                'link_karma': self.link_karma
            }
