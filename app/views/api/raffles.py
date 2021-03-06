from flask import jsonify, request, session, url_for
from datetime import timezone

from app.jobs.raffle_job import raffle
from app.util.raffle_form_validator import RaffleFormValidator
from app.services import reddit_service
from app.db.models.user import User
from app.db.models.raffle import Raffle


def new_raffle():
    """ Accepts a form with key values in raffles/new.html. Returns 422 if
    form validation fails, else queues job and returns 202. """
    validator = RaffleFormValidator(request.form.to_dict())
    if not validator.run():
        return jsonify({"message": "Form validation failed."}), 422

    form = validator.get_sanitized_form()
    user = User.find_by_jwt(session["jwt"]) if "jwt" in session else None
    sub_id = reddit_service.get_submission_by_url(form["submissionUrl"])["id"]

    raffle.queue(
        raffle_params={
            "submission_url": form["submissionUrl"],
            "winner_count": form["winnerCount"],
            "min_account_age": form["minAge"],
            "min_comment_karma": form.get("minComment"),
            "min_link_karma": form.get("minLink"),
            "min_combined_karma": form.get("minCombined"),
            "ignored_users": form["ignoredUsers"],
        },
        user=user,
        job_id=sub_id,
    )

    return jsonify({"url": url_for("raffles.status", job_id=sub_id)}), 202


def get_raffle_metrics():
    return jsonify(Raffle.get_vanity_metrics())


def get_recent_raffles():
    # Don't expose more fields than we need to.
    return jsonify(
        [
            {
                "created_at": r.created_at.replace(tzinfo=timezone.utc).timestamp(),
                "submission_title": r.submission_title,
                "submission_id": r.submission_id,
                "subreddit": r.subreddit,
                "url_path": url_for("raffles.show", submission_id=r.submission_id),
            }
            for r in Raffle.get_recent_raffles()
        ]
    )


RouteConfigs = [
    {"rule": "/raffles/new", "view_func": new_raffle, "methods": ["POST"]},
    {"rule": "/raffles/metrics", "view_func": get_raffle_metrics},
    {"rule": "/raffles/recent", "view_func": get_recent_raffles},
]
