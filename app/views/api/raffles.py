from flask import jsonify, request, session, url_for

from app.jobs.raffle_job import raffle

from app.util.raffle_form_validator import RaffleFormValidator
from app.services import reddit_service
from app.db.models.user import User


def new_raffle():
    """ Accepts a form with key values in raffles/new.html. Returns 422 if
    form validation fails, else queues job and returns 202. """
    validator = RaffleFormValidator(request.form.to_dict())
    if not validator.run():
        return jsonify({"message": "Form validation failed."}), 422

    form = validator.get_sanitized_form()
    user = User.find_by_jwt(session["jwt"]) if "jwt" in session else None
    sub_id = reddit_service.get_submission_by_url(form["submissionUrl"])["id"]

    raffle.queue(raffle_params=_raffle_params_from_form(form), user=user, job_id=sub_id)

    return jsonify({"url": url_for("raffles.status", job_id=sub_id)}), 202


def _raffle_params_from_form(form):
    return {
        "submission_url": form["submissionUrl"],
        "winner_count": form["winnerCount"],
        "min_account_age": form["minAge"],
        "min_comment_karma": form.get("minComment"),
        "min_link_karma": form.get("minLink"),
        "min_combined_karma": form.get("minCombined"),
        "ignored_users": form["ignoredUsers"],
    }


RouteConfigs = [{"rule": "/raffles/new", "view_func": new_raffle, "methods": ["POST"]}]

