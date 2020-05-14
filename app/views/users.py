from flask import Blueprint, jsonify

from app.extensions import csrf
from app.db.models.user import User

user = Blueprint("api_users", __name__)
# csrf.exempt(user)


@user.route("/<username>")
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(error_message=f"User '{username}' not found"), 404

    return jsonify(user.get_profile())
