from flask import abort, Blueprint, render_template
from app.db.models.user import User

users = Blueprint("users", __name__)


@users.route("/<username>")
def show(username):
    user = User.query.filter_by(username=username).one_or_none()
    if not user:
        abort(404)
    return render_template(
        "users/show.html", title="/u/%s's Raffles" % user.username, user=user
    )
