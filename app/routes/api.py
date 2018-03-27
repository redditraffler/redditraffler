from flask import (
    abort,
    Blueprint,
    current_app,
    jsonify,
    redirect,
    request,
    session,
    url_for
)
from app.util import reddit
from app.extensions import rq
from app.db.models import Raffle
from app.jobs.raffle_job import raffle
import ast
import re


api = Blueprint('api', __name__)


@api.route('/submissions')
def submissions():
    """ Return the user's Reddit submissions, filtering out submissions
    that have already been made into raffles. """

    if 'reddit_refresh_token' not in session:
        abort(401)

    submissions = reddit.get_user_submissions(session['reddit_refresh_token'])
    return jsonify(_filter_submissions(submissions) if submissions else None)


@api.route('/submission')
def submission():
    """ Accepts a `url` parameter and returns the associated submission. If
    a raffle exists for the given submission then the path to that raffle is
    returned. """

    if not request.args.get('url'):
        abort(400)

    url = request.args.get('url')
    sub_id = reddit.submission_id_from_url(url)

    if Raffle.query.filter_by(submission_id=sub_id).scalar():
        return jsonify({
            'url': url_for('raffles.show', submission_id=sub_id)
        }), 303
    else:
        submission = reddit.get_submission(sub_url=url)
        return jsonify(submission) if submission else abort(404)


@api.route('/job_status')
def status():
    job = rq.get_queue().fetch_job(request.args.get('job_id'))
    if not job:
        abort(404)

    status = job.meta.get('status') if 'status' in job.meta \
        else 'Waiting to process...'

    return jsonify({'status': status, 'error': job.meta.get('error')})


@api.route('/raffles/new', methods=['POST'])
def new_raffle():
    form = request.form.copy()
    if 'submissionUrl' in form:
        form['submissionUrl'] = _ensure_protocol(form['submissionUrl'])
    if not _validate_raffle_form(form):
        current_app.logger.error('Form validation failed {}'.format(
            [(key, value) for key, value in request.form.items()]))
        return jsonify({'message': 'Form validation failed.'}), 422

    sub_id = reddit.submission_id_from_url(form.get('submissionUrl'))
    if _raffle_exists(sub_id):
        return jsonify({
            'url': url_for('raffles.show', submission_id=sub_id)
        }), 303

    user = _try_get_user_from_session()
    raffle.queue(raffle_params=_raffle_params_from_form(form),
                 user=user,
                 job_id=sub_id)
    return jsonify({'url': url_for('raffles.status', job_id=sub_id)}), 202


def _filter_submissions(submissions_list):
    existing_raffle_ids = [tuple[0] for tuple in Raffle.query.
                           with_entities(Raffle.submission_id).all()]
    return [sub for sub in submissions_list if
            sub['id'] not in existing_raffle_ids]


def _validate_raffle_form(form):
    # Validate presence of required keys.
    REQUIRED_KEYS = {'submissionUrl', 'winnerCount', 'minAge', 'minComment',
                     'minLink', 'ignoredUsers'}
    if not REQUIRED_KEYS.issubset(form.keys()):
        return False

    # Validate integer-value keys.
    # All values must be non-negative. winnerCount must be at least 1.
    INT_KEYS = {'minAge', 'winnerCount', 'minComment', 'minLink'}
    for key in INT_KEYS:
        val = form.get(key, type=int)
        if (not isinstance(val, int)) or (val < 0) or \
           (key == 'winnerCount' and (val < 1 or val > 25)):
            return False

    # Validate that the submission exists
    url = _ensure_protocol(form.get('submissionUrl'))
    if not reddit.get_submission(sub_url=url):
        return False

    # Validate ignored users list
    try:
        users_list = ast.literal_eval(form.get('ignoredUsers'))
        assert isinstance(users_list, list)
    except (SyntaxError, ValueError, AssertionError):
        return False
    USERNAME_REGEX = r'\A[\w-]+\Z'
    for username in users_list:
        if not isinstance(username, str) or len(username) < 3 or \
           len(username) > 20 or not re.match(USERNAME_REGEX, username):
            return False

    return True


def _ensure_protocol(url):
    if url.startswith('http'):
        return url
    return 'https://' + url


def _try_get_user_from_session():
    if 'reddit_username' in session:
        return User.query \
                   .filter_by(username=session['reddit_username']) \
                   .first()
    else:
        return None


def _raffle_params_from_form(form):
    return {
        'submission_url': form.get('submissionUrl'),
        'winner_count': form.get('winnerCount', type=int),
        'min_account_age': form.get('minAge', type=int),
        'min_comment_karma': form.get('minComment', type=int),
        'min_link_karma': form.get('minLink', type=int),
        'ignored_users': ast.literal_eval(form.get('ignoredUsers'))
    }


def _raffle_exists(sub_id):
    return Raffle.query.filter_by(submission_id=sub_id).scalar()
