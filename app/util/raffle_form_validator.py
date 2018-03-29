from flask import current_app
from app.util import reddit
from app.db.models import Raffle
import ast
import re


class RaffleFormValidator():
    REQUIRED_KEYS = {'submissionUrl', 'winnerCount', 'minAge',
                     'minComment', 'minLink', 'ignoredUsers'}
    INT_KEYS = {'minAge', 'winnerCount', 'minComment', 'minLink'}

    def __init__(self, form):
        """ form must be a dict. """
        self.form = form

    def run(self):
        """ Run all validations. Returns True if validations pass,
        else False. """
        try:
            self._validate_required_keys()
            self._validate_int_values()
            self._validate_submission_url()
            self._validate_raffle_not_exists()
            self._validate_ignored_users_list()
            return True
        except:
            current_app.logger.exception('Form validation failed {}'.format(
                [(key, value) for key, value in self.form.items()]))
            return False

    def get_sanitized_form(self):
        self._sanitize_url()
        self._cast_int_values()
        return self.form

    def _validate_required_keys(self):
        for key in self.REQUIRED_KEYS:
            if key not in self.form.keys():
                raise KeyError('Missing key {}'.format(key))

    def _validate_int_values(self):
        """ Check if all integer keys have proper values. """
        for key in self.INT_KEYS:
            val = self.try_cast_int(self.form.get(key))
            if not isinstance(val, int):
                raise TypeError('Invalid type for key {}: {}'.format(key, val))
            if (val < 0) or \
               ((key == 'winnerCount') and (val < 1 or val > 25)):
                raise ValueError('Invalid value for key {}: {}'
                                 .format(key, val))

    def _validate_submission_url(self):
        """ Use PRAW to check if the submission URL is valid. """
        url = self.form.get('submissionUrl')
        if not isinstance(url, str):
            raise TypeError('{} is not a string'.format(url))
        url = self.ensure_protocol(url)
        if not reddit.get_submission(sub_url=url):
            raise ValueError('Invalid submission url: {}'.format(url))

    def _validate_raffle_not_exists(self):
        """ Checks that the submission URL given has not already been made
        into a raffle. """
        url = self.ensure_protocol(self.form.get('submissionUrl'))
        sub_id = reddit.submission_id_from_url(url)
        if Raffle.query.filter_by(submission_id=sub_id).scalar():
            raise ValueError("Raffle already exists for {}".format(sub_id))

    def _validate_ignored_users_list(self):
        """ Check that ignoredUsers is a list, and all of its contents
        are valid Reddit usernames. """
        try:
            users_list = ast.literal_eval(self.form.get('ignoredUsers'))
            assert isinstance(users_list, list)
        except:
            raise TypeError('users_list is of type {}. Expected: list'
                            .format(type(self.form.get('ignoredUsers'))))

        USERNAME_REGEX = r'\A[\w-]+\Z'
        for username in users_list:
            if (len(username) < 3) or \
               (len(username) > 20) or \
               (not re.match(USERNAME_REGEX, username)):
                raise ValueError('Invalid username: {}'.format(username))

    def _sanitize_url(self):
        self.form['submissionUrl'] = self.\
            ensure_protocol(self.form['submissionUrl'])

    def _cast_int_values(self):
        for key in self.INT_KEYS:
            self.form[key] = int(self.form[key])

    @staticmethod
    def try_cast_int(x):
        try:
            return int(x)
        except:
            return x

    @staticmethod
    def ensure_protocol(url):
        if not url.startswith('http'):
            return 'https://' + url
        return url
