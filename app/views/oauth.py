from flask import Blueprint, jsonify, request
from app.services import reddit_service

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

    auth_code = request.get_json().get("code")
    try:
        refresh_token = reddit_service.authorize(code=auth_code)
        # Save refresh token to user
        # Generate JWT
        # Return JWT
    except:
        return jsonify(error_message=FAILED_AUTH_CODE_AUTHORIZATION_MESSAGE), 500

