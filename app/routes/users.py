from flask import (
    abort,
    Blueprint,
    render_template
)
from app.db import db
from app.db.models import User

users = Blueprint('users', __name__)


@users.route('/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).one_or_none()

    if not user:
        abort(404)

    raffles = user.raffles
    return render_template('users/show_user.html',
                           user=user,
                           raffles=raffles)
