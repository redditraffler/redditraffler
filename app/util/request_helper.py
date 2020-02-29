from functools import wraps
from flask import session, abort, current_app
from app.util import JwtHelper


class RequestHelper:
    @staticmethod
    def require_login(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            if ("jwt" not in session) and ("reddit_username" not in session):
                return abort(401)

            jwt = session["jwt"]
            try:
                JwtHelper.decode(jwt)
            except:
                current_app.logger.exception("Failed to decode JWT", {"jwt": jwt})
                return abort(401)

            return f(*args, **kwargs)

        return decorated_fn
