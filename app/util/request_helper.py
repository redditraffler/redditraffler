from functools import wraps
from flask import session, abort, current_app, request, jsonify
from app.util import jwt_helper
from app.db.models.user import User


def require_login(f):
    @wraps(f)
    def decorated_fn(*args, **kwargs):
        if ("jwt" not in session) and ("reddit_username" not in session):
            return abort(401)

        jwt = session["jwt"]
        try:
            jwt_helper.decode(jwt)
        except:
            current_app.logger.exception("Failed to decode JWT", {"jwt": jwt})
            return abort(401)

        return f(*args, **kwargs)

    return decorated_fn


def require_jwt(f):
    @wraps(f)
    def decorated_fn(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if len(auth_header.split("Bearer ")) != 2:
            return jsonify(error_message="Invalid or missing Authorization header"), 401

        try:
            jwt = auth_header.split("Bearer ")[1]
            user = User.find_by_jwt(jwt)
            kwargs["user"] = user
        except:
            current_app.logger.exception("Failed to fetch user by JWT", {"jwt": jwt})
            return jsonify(error_message="Invalid Authorization header"), 401

        return f(*args, **kwargs)

    return decorated_fn
