from datetime import datetime

from flask import current_app
import praw
import prawcore
import random

from app.config import BaseConfig as config


class Raffler:
    def __init__(
        self,
        submission_url,
        winner_count,
        min_account_age,
        min_comment_karma,
        min_link_karma,
        min_combined_karma,
        ignored_users,
    ):
        """ Initialize a Reddit instance and helper data structures,
        fetch the submission, and set all raffle parameters. """
        self.reddit = praw.Reddit(
            client_id=config.BOT_CLIENT_ID,
            client_secret=config.BOT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT,
            username=config.BOT_USERNAME,
            password=config.BOT_PASSWORD,
        )
        self.submission = self.reddit.submission(url=submission_url)
        self.winner_count = int(winner_count)
        self.min_account_age = int(min_account_age)
        self.min_comment_karma = (
            int(min_comment_karma) if min_comment_karma is not None else None
        )
        self.min_link_karma = (
            int(min_link_karma) if min_link_karma is not None else None
        )
        self.min_combined_karma = (
            int(min_combined_karma) if min_combined_karma is not None else None
        )

        self._winners = {}
        self._entries = set()
        self._disqualified_users = set([u.lower() for u in ignored_users])

    def fetch_comments(self):
        """ Fetch the submission's comments in a random order.
        `replace_more(limit=20)` is equivalent to scrolling down in a
        submission to load more comments. Top-level, valid comments are
        then added to an internal set `_entries`. Returns whether the
        loop succeeded in finding at least as many entries as
        `winner_count`. """
        self.submission.comment_sort = "random"
        self.submission.comments.replace_more(limit=20)
        for comment in self.submission.comments.list():
            if (comment not in self._entries) and self._is_valid_comment(comment):
                self._entries.add(comment)

        if len(self._entries) < self.winner_count:
            err_msg = "Could not fetch enough valid comments to select winners"
            current_app.logger.error(
                err_msg,
                {
                    "winner_count": self.winner_count,
                    "valid_comments": len(self._entries),
                },
            )
            raise ValueError(err_msg)

    def select_winners(self):
        """ Loop over the internal set of entries to find comments whose
        author meets the criteria set. Authors that meet the criteria are
        added to an internal dict `_winners`. Returns whether the loop
        succeeded in finding enough winners to match `winner_count`.
        """
        while (len(self._entries) > 0) and (len(self._winners) < self.winner_count):
            entry = random.choice(tuple(self._entries))
            self._entries.remove(entry)

            user = self._try_create_user(entry.author)
            if user and self._is_valid_winner(user):
                self._winners.update({user: entry})

        if len(self._winners) < self.winner_count:
            err_msg = "Could not find enough eligible winners for this raffle"
            current_app.logger.error(
                err_msg,
                {
                    "winner_count": self.winner_count,
                    "eligible_winners_selected": len(self._winners),
                },
            )
            raise ValueError(err_msg)

    def get_serialized_winners(self):
        result = []
        for user, comment in self._winners.items():
            result.append(
                {
                    "user": user.as_dict(),
                    "comment_url": "https://reddit.com" + comment.permalink,
                }
            )
        return result

    def _is_valid_comment(self, comment):
        """ Returns true if the comment is in the raffle's submission, and
        it is not banned or removed. """
        try:
            return (
                (comment.is_root)
                and (comment.body is not None)
                and (comment.author is not None)
                and self._is_same_submission(comment)
            )
        except:
            current_app.logger.exception(
                "Failed to check if comment is valid", {"comment": comment}
            )
            return False

    def _is_valid_winner(self, user):
        """ Returns true if the user meets the raffle requirements and it
        the user only has one comment in the raffle submission. """
        try:
            if (
                (user.username.lower() not in self._disqualified_users)
                and (user.age >= self.min_account_age)
                and self._user_has_sufficient_karma(user)
                and (not self._has_duplicate_comments(user))
            ):
                return True
            else:
                self._disqualified_users.add(user.username.lower())
                return False
        except:
            current_app.logger.exception(
                "Error while trying to determine if user meets raffle criteria",
                {"user": user},
            )
            return False

    def _user_has_sufficient_karma(self, user):
        if self.min_combined_karma is not None:
            return (user.comment_karma + user.link_karma) >= self.min_combined_karma
        elif self.min_comment_karma is not None and self.min_comment_karma is not None:
            return (user.comment_karma >= self.min_comment_karma) and (
                user.link_karma >= self.min_link_karma
            )

    def _try_create_user(self, author):
        """ Utility function to make sure the author of an entry isn't banned
        or anything along those lines. """
        try:
            user = self.User(
                username=author.name,
                age=Raffler._account_age_days(author.created_utc),
                comment_karma=author.comment_karma,
                link_karma=author.link_karma,
            )
            return user
        except (prawcore.exceptions.NotFound, AttributeError):
            current_app.logger.exception(
                "Error while trying to create user from comment entry",
                {"author": author},
            )
            return None

    def _has_duplicate_comments(self, user):
        """ Returns if the user has more than one root comment in the raffle's
        submission. If there is more than one then the user is added to
        the disqualified users set.
        """
        # NOTE: Praw can only fetch 1k comments at most, so we return if
        # count > 1 in the case that the submission is old enough that we
        # aren't able to fetch comments (count == 0) from that submission.
        count = 0
        comments = self.reddit.redditor(user.username).comments.new(limit=None)
        for comment in comments:
            if (comment.created_utc < self.submission.created_utc) or (count > 1):
                break
            if self._is_valid_comment(comment):
                count += 1
        return count > 1

    def _is_same_submission(self, comment):
        """ Utility function to check if comment's submission is same as
        the raffle's submission """
        return comment.submission.id == self.submission.id

    @staticmethod
    def _account_age_days(created_utc):
        """ Utility function to get account age in days. """
        return (datetime.utcnow() - datetime.utcfromtimestamp(created_utc)).days

    class User:
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
                "username": self.username,
                "age": self.age,
                "comment_karma": self.comment_karma,
                "link_karma": self.link_karma,
            }
