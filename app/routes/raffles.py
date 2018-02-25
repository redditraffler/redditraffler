from flask import (
    abort,
    Blueprint,
    render_template,
    request,
    url_for
)
from app.util import reddit

raffles = Blueprint('raffles', __name__)


@raffles.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('raffles/create.html',
                               title='create a raffle',
                               reddit_login_url=reddit.get_auth_url())
    elif request.method == 'POST':
        if not _validate_raffle_form(request.form):
            abort(422)
        return 'ok'


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
        if (key == 'winnerCount' and form.get(key, type=int) < 1) or \
           (form.get(key, type=int) < 0):
            return False

    # Validate submission validity
    if not reddit.get_submission(sub_url=form.get('submissionUrl')):
        return False

    return True
