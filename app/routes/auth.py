from flask import abort, Blueprint, current_app, redirect, request, session, url_for

from app.db.models import User
from app.services import reddit_service

auth = Blueprint("auth", __name__)


@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("base.index"))


@auth.route("/redirect")
def auth_redirect():
    if request.args.get("error") == "access_denied":
        current_app.logger.warning("User declined Reddit authorization")
        return redirect(url_for("base.index"))
    if ("jwt" in session) and ("reddit_username" in session):
        return redirect(url_for("base.index"))

    try:
        auth_code = request.args.get("code")
        refresh_token = reddit_service.authorize(auth_code)
        reddit_user = reddit_service.get_user_from_token(refresh_token)
        username = reddit_user.name

        user = User.find_or_create(username)
        user.set_refresh_token(refresh_token)
        jwt = user.get_jwt()

        session["jwt"] = jwt
        session["reddit_username"] = username

        return redirect(url_for("raffles.new"))
    except:
        current_app.logger.exception("Reddit auth redirect failure")
        abort(500)
