from flask import (
    abort,
    Blueprint,
    render_template
)
from app.extensions import db
from app.db.models import User, Raffle

users = Blueprint('users', __name__)


@users.route('/<username>')
def show(username):
    user = User.query.filter_by(username=username).one_or_none()

    if not user:
        abort(404)

    raffles = Raffle.query.filter_by(user_id=user.id) \
                          .order_by('created_at desc')

    return render_template('users/show.html',
                           title='/u/' + user.username,
                           user=user,
                           raffles=raffles)
