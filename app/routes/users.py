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
    if not User.query.filter_by(username=username).scalar():
        abort(404)

    user = User.query.filter_by(username=username).one()
    raffles = user.raffles

    return 'user found!'
