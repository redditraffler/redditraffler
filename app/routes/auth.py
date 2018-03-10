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
from app.extensions import db, csrf
from app.db.models import User

auth = Blueprint('auth', __name__)


@auth.route('/logout', methods=['POST'])
@csrf.exempt
def logout():
    session.clear()
    # Flash message
    return redirect(url_for('base.index'))


@auth.route('/redirect')
def auth_redirect():
    if request.args.get('error') == 'access_denied':
        # User clicked deny access
        abort(500)

    # Possible prawcore.exceptions.OAuthException here

    refresh_token = reddit.authorize(request.args.get('code'))
    username = reddit.get_username(refresh_token)

    session['reddit_refresh_token'] = refresh_token
    session['reddit_username'] = username

    if not User.query.filter_by(username=username).scalar():
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('raffles.new'))
