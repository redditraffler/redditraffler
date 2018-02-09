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

get = Blueprint('get', __name__)


@get.route('/')
def index():
    return render_template(
        'index.html',
        title='Home',
        reddit_login_url=reddit.get_auth_url()
    )


@get.route('/auth_redirect')
def auth_redirect():
    if request.args.get('error') == 'access_denied':
        # User clicked deny access
        abort(500)
    elif request.args.get('state') != 'authorized':
        abort(500)

    refresh_token = reddit.authorize(request.args.get('code'))
    session['reddit_refresh_token'] = refresh_token
    session['reddit_username'] = reddit.get_username(refresh_token)
    return redirect(url_for('get.raffle_form'))


@get.route('/raffles/create')
def raffle_form():
    return render_template('raffle_form.html')
