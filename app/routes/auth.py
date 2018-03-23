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
from app.extensions import db
from app.db.models import User

auth = Blueprint('auth', __name__)


@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('base.index'))


@auth.route('/redirect')
def auth_redirect():
    if request.args.get('error') == 'access_denied':
        current_app.logger.info('User declined Reddit authorization')
        return redirect(url_for('base.index'))
    if 'reddit_refresh_token' in session:
        current_app.logger.info('User already logged in')
        return redirect(url_for('base.index'))

    try:
        refresh_token = reddit.authorize(request.args.get('code'))
        username = reddit.get_username(refresh_token)

        session['reddit_refresh_token'] = refresh_token
        session['reddit_username'] = username

        if not User.query.filter_by(username=username).scalar():
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
    except:
        current_app.logger.exception('Exception in auth redirect')
        abort(500)

    return redirect(url_for('raffles.new'))
