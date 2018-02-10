from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from app.lib import reddit

auth = Blueprint('auth', __name__)


@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    # Flash message
    return redirect(url_for('base.index'))


@auth.route('/redirect')
def auth_redirect():
    if request.args.get('error') == 'access_denied':
        # User clicked deny access
        abort(500)
    elif request.args.get('state') != 'authorized':
        abort(500)

    refresh_token = reddit.authorize(request.args.get('code'))
    session['reddit_refresh_token'] = refresh_token
    session['reddit_username'] = reddit.get_username(refresh_token)
    return redirect(url_for('raffle.form'))
