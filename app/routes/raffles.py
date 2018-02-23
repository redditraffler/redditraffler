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

raffles = Blueprint('raffles', __name__)


@raffles.route('/create')
def create():
    return render_template('raffles/create.html',
                           title='create a raffle',
                           reddit_login_url=reddit.get_auth_url())
