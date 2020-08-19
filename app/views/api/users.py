from flask import abort, jsonify, session

from app.util import request_helper
from app.services import reddit_service
from app.db.models.raffle import Raffle
from app.db.models.user import User


@request_helper.require_login
def get_user_submissions():
    """ Return the user's Reddit submissions that are not already made
    into raffles. """
    user = User.find_by_jwt(session["jwt"])
    if not user:
        abort(401)

    submissions = reddit_service.get_submissions_for_user(user.get_refresh_token())

    if len(submissions) == 0:
        return jsonify([])

    # Remove submissions that were already made into raffles.
    existing_verified_raffle_ids = set(
        [r.submission_id for r in Raffle.get_verified_raffles()]
    )
    filtered_submissions = [
        submission
        for submission in submissions
        if submission["id"] not in existing_verified_raffle_ids
    ]

    return jsonify(filtered_submissions)


def get_user_raffles(username):
    """ Returns all the raffles that were created by the given user. """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found."}), 404
    return jsonify([r.as_dict() for r in user.raffles])


RouteConfigs = [
    {"rule": "/submissions", "view_func": get_user_submissions},
    {"rule": "/users/<username>/raffles", "view_func": get_user_raffles},
]
