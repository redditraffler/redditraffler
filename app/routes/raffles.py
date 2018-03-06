from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from app.util import reddit
from app.jobs.raffle_job import raffle
from app.db.models import User, Raffle
from app.extensions import rq

raffles = Blueprint('raffles', __name__)


@raffles.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('raffles/create.html',
                               title='create a raffle',
                               reddit_login_url=reddit.get_auth_url())
    elif request.method == 'POST':
        form = request.form.copy()
        if 'submissionUrl' in form:
            form['submissionUrl'] = _ensure_protocol(form['submissionUrl'])
        if not _validate_raffle_form(form):
            abort(422)

        user = _try_get_user_from_session()
        sub_id = reddit.submission_id_from_url(form.get('submissionUrl'))
        raffle_params = {
            'submission_url': form.get('submissionUrl'),
            'winner_count': form.get('winnerCount', type=int),
            'min_account_age': form.get('minAge', type=int),
            'min_comment_karma': form.get('minComment', type=int),
            'min_link_karma': form.get('minLink', type=int)
        }

        raffle.queue(raffle_params=raffle_params,
                     user=user,
                     job_id=sub_id)
        return redirect(url_for('raffles.status', job_id=sub_id))


@raffles.route('/<job_id>/status')
def status(job_id):
    if not rq.get_queue().fetch_job(job_id):
        abort(404)
    return render_template('raffles/status.html',
                           title='raffle status',
                           job_id=job_id)


@raffles.route('/<submission_id>')
def show(submission_id):
    raffle = Raffle.query.filter_by(submission_id=submission_id).first()
    if not raffle:
        abort(404)
    title = 'results for "%s"' % raffle.submission_title
    return render_template('raffles/show.html',
                           title=title,
                           raffle=raffle)


def _validate_raffle_form(form):
    # Validate presence of required keys.
    REQUIRED_KEYS = {'submissionUrl', 'winnerCount', 'minAge', 'minComment',
                     'minLink'}
    if not REQUIRED_KEYS.issubset(form.keys()):
        return False

    # Validate integer-value keys.
    # All values must be non-negative. winnerCount must be at least 1.
    INT_KEYS = {'minAge', 'winnerCount', 'minComment', 'minLink'}
    for key in INT_KEYS:
        val = form.get(key, type=int)
        if (not isinstance(val, int)) or (val < 0) or \
           (key == 'winnerCount' and val < 1):
            return False

    # Validate that the submission exists
    url = _ensure_protocol(form.get('submissionUrl'))
    if not reddit.get_submission(sub_url=url):
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
