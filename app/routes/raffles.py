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
