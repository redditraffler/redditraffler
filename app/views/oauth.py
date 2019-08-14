# NOTE: This module/blueprint should only be used as an API backend for an SPA
# front-end. It's currently a dead code path.

from flask import Blueprint, jsonify, request

from app.services import reddit_service
from app.db.models import User

oauth = Blueprint("oauth", __name__)


MISSING_AUTH_CODE_MESSAGE = "Authorization code is required."
FAILED_AUTH_CODE_AUTHORIZATION_MESSAGE = "Failed to authorize the given code."


@oauth.route("/get_reddit_oauth_url")
def get_reddit_oauth_url():
    return jsonify(reddit_oauth_url=reddit_service.get_oauth_url())


@oauth.route("/authorize_code", methods=["POST"])
def authorize_oauth_code():
    if not (request.get_json() or request.get_json().get("code")):
        return jsonify(error_message=MISSING_AUTH_CODE_MESSAGE), 400

    try:
        auth_code = request.get_json().get("code")

        refresh_token = reddit_service.authorize(code=auth_code)
        reddit_user = reddit_service.get_user_from_token(refresh_token)

        user = User.find_or_create(reddit_user.username)
        user.set_refresh_token(refresh_token)
        jwt = user.get_jwt()

        return jsonify(jwt=jwt)
    except:
        return jsonify(error_message=FAILED_AUTH_CODE_AUTHORIZATION_MESSAGE), 500

