import re
import json

from flask import current_app

from app.services import reddit_service
from app.db.models.raffle import Raffle


class RaffleFormValidator:
    REQUIRED_KEYS = {"submissionUrl", "winnerCount", "minAge", "ignoredUsers"}
    INT_KEYS = {"minAge", "winnerCount", "minComment", "minLink", "minCombined"}
    KARMA_KEYS = {"split": ["minComment", "minLink"], "combined": ["minCombined"]}
    MIN_WINNER_COUNT = 1
    MAX_WINNER_COUNT = 100

    def __init__(self, form):
        """ form must be a dict. """
        self.form = form

    def run(self):
        """ Run all validations. Returns True if validations pass,
        else False. """
        try:
            self._validate_required_keys()
            self._validate_karma_keys()
            self._validate_int_values()
            self._validate_submission_url()
            self._validate_raffle_not_exists()
            self._validate_ignored_users_list()
            return True
        except:
            current_app.logger.exception(
                "Raffle form validation failed", {"form": self.form}
            )
            return False

    def get_sanitized_form(self):
        self._sanitize_url()
        self._cast_int_values()
        self._cast_ignored_users_list()
        return self.form

    def _validate_required_keys(self):
        for key in self.REQUIRED_KEYS:
            if key not in self.form.keys():
                raise KeyError("Missing key {}".format(key))

    def _validate_karma_keys(self):
        """ Performs an XOR check on (minComment, minLink) and (minCombined) form keys
        """
        form_keys = self.form.keys()

        def is_subarray_in_array(subarray, array):
            return all(s in array for s in subarray)

        is_split_keys_in_form = is_subarray_in_array(
            self.KARMA_KEYS["split"], form_keys
        )
        is_combined_keys_in_form = is_subarray_in_array(
            self.KARMA_KEYS["combined"], form_keys
        )

        if not is_split_keys_in_form and not is_combined_keys_in_form:
            raise KeyError(
                "Either both split karma keys or the combined karma key must be present"
            )

        if is_split_keys_in_form and is_combined_keys_in_form:
            raise KeyError(
                "Cannot have both karma keys and combined karma keys in the same form"
            )

    def _validate_int_values(self):
        """ Check if all integer keys have proper values. """
        for key, val in self.form.items():
            if key not in self.INT_KEYS:
                continue

            val = self.try_cast_int(self.form.get(key))
            if not isinstance(val, int):
                raise TypeError("Invalid type for key {}: {}".format(key, val))
            if (val < 0) or (
                (key == "winnerCount")
                and not (self.MIN_WINNER_COUNT <= val <= self.MAX_WINNER_COUNT)
            ):
                raise ValueError("Invalid value for key {}: {}".format(key, val))

    def _validate_submission_url(self):
        """ Use PRAW to check if the submission URL is valid. """
        url = self.form.get("submissionUrl")
        if not isinstance(url, str):
            raise TypeError("{} is not a string".format(url))
        url = self.ensure_protocol(url)
        if not reddit_service.get_submission_by_url(url):
            raise ValueError("Invalid submission url: {}".format(url))

    def _validate_raffle_not_exists(self):
        """ Checks that the submission URL given has not already been made
        into a verified raffle. """
        url = self.ensure_protocol(self.form.get("submissionUrl"))
        submission = reddit_service.get_submission_by_url(url)
        has_existing_raffle = (
            Raffle.query.filter(Raffle.submission_id == submission["id"])
            .filter(Raffle.user_id.isnot(None))
            .scalar()
        )
        if has_existing_raffle:
            raise ValueError("Raffle already exists for {}".format(submission["id"]))

    def _validate_ignored_users_list(self):
        """ Check that ignoredUsers is a list, and all of its contents
        are valid Reddit usernames. """
        try:
            users_list = json.loads(self.form.get("ignoredUsers"))
            assert isinstance(users_list, list)
        except:
            raise TypeError(
                "users_list is of type {}. Expected: list".format(
                    type(self.form.get("ignoredUsers"))
                )
            )

        USERNAME_REGEX = r"\A[\w-]+\Z"
        for username in users_list:
            if (
                (len(username) < 3)
                or (len(username) > 20)
                or (not re.match(USERNAME_REGEX, username))
            ):
                raise ValueError("Invalid username: {}".format(username))

    def _sanitize_url(self):
        self.form["submissionUrl"] = self.ensure_protocol(self.form["submissionUrl"])

    def _cast_int_values(self):
        for key in self.form:
            if key in self.INT_KEYS:
                self.form[key] = int(self.form[key])

    def _cast_ignored_users_list(self):
        self.form["ignoredUsers"] = json.loads(self.form.get("ignoredUsers"))

    @staticmethod
    def try_cast_int(x):
        try:
            return int(x)
        except:
            return x

    @staticmethod
    def ensure_protocol(url):
        if not url.startswith("http"):
            return "https://" + url
        return url
