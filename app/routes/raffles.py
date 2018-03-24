from flask import (
    abort,
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from app.util import reddit
from app.jobs.raffle_job import raffle
from app.db.models import User, Raffle
from app.extensions import rq, cache, db

raffles = Blueprint('raffles', __name__)


@raffles.route('')
def index():
    raffles = Raffle.query.all()
    return render_template('raffles/index.html',
                           title='View All Raffles',
                           raffles=raffles)


@raffles.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('raffles/new.html',
                               title='New Raffle',
                               reddit_login_url=reddit.get_auth_url())
    elif request.method == 'POST':
        form = request.form.copy()
        if 'submissionUrl' in form:
            form['submissionUrl'] = _ensure_protocol(form['submissionUrl'])
        if not _validate_raffle_form(form):
            current_app.logger.error('Form validation failed {}'.format(
                [(key, value) for key, value in request.form.items()]))
            abort(422)

        sub_id = reddit.submission_id_from_url(form.get('submissionUrl'))
        if _raffle_exists(sub_id):
            return redirect(url_for('raffles.show', submission_id=sub_id))

        user = _try_get_user_from_session()
        raffle.queue(raffle_params=_raffle_params_from_form(form),
                     user=user,
                     job_id=sub_id)
        return redirect(url_for('raffles.status', job_id=sub_id))


@raffles.route('/<job_id>/status')
def status(job_id):
    if not rq.get_queue().fetch_job(job_id):
        abort(404)
    return render_template('raffles/status.html',
                           title='Raffle Status',
                           job_id=job_id)


@raffles.route('/<submission_id>')
def show(submission_id):
    raffle = _raffle_from_cache(submission_id)
    if not raffle:
        abort(404)
    return render_template('raffles/show.html',
                           title='Results For "%s"' % raffle.submission_title,
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
           (key == 'winnerCount' and (val < 1 or val > 25)):
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


def _raffle_params_from_form(form):
    return {
        'submission_url': form.get('submissionUrl'),
        'winner_count': form.get('winnerCount', type=int),
        'min_account_age': form.get('minAge', type=int),
        'min_comment_karma': form.get('minComment', type=int),
        'min_link_karma': form.get('minLink', type=int)
    }


def _raffle_exists(sub_id):
    return Raffle.query.filter_by(submission_id=sub_id).scalar()


def _raffle_from_cache(sub_id):
    cache_key = 'raffle_{}'.format(sub_id)
    cached = cache.get(cache_key)
    if not cached:
        raffle = Raffle.query.filter_by(submission_id=sub_id).first()
        if raffle:
            cache.set(cache_key, raffle)
    else:
        db.session.add(cached)
        raffle = cached
    return raffle
