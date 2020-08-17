from flask import abort, Blueprint, jsonify, request, session, url_for

from app.extensions import rq
from app.jobs.raffle_job import raffle
from app.util import request_helper
from app.util.raffle_form_validator import RaffleFormValidator
from app.services import reddit_service
from app.db.models.raffle import Raffle
from app.db.models.user import User


api = Blueprint("api", __name__)


@api.route("/submissions")
@request_helper.require_login
def submissions():
    """ Return the user's Reddit submissions that are not already made
    into raffles. """
    user = User.find_by_jwt(session["jwt"])
    if not user:
        abort(401)

    submissions = reddit_service.get_submissions_for_user(user.get_refresh_token())
    return jsonify(_filter_submissions(submissions) if submissions else [])


@api.route("/submission")
def submission():
    """ Accepts a `url` parameter and returns the associated submission. If the
    submission does not exist, a 404 is returned. If a raffle exists for the
    given submission then the path to that raffle is returned. """
    if not request.args.get("url"):
        abort(400)

    url = request.args.get("url")
    submission = reddit_service.get_submission_by_url(url)
    if not submission:
        abort(404)

    sub_id = submission["id"]
    has_existing_raffle = Raffle.query.filter_by(submission_id=sub_id).scalar()

    if has_existing_raffle:
        return jsonify({"url": url_for("raffles.show", submission_id=sub_id)}), 303
    else:
        return jsonify(submission)


@api.route("/job_status")
def status():
    """ Returns the job status for a given raffle job. """
    job = rq.get_queue().fetch_job(request.args.get("job_id"))
    if not job:
        abort(404)

    status = job.meta.get("status") if "status" in job.meta else "Waiting to process..."

    return jsonify({"status": status, "error": job.meta.get("error")})


@api.route("/raffles/new", methods=["POST"])
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


@api.route("/users/<username>/raffles")
def get_user_raffles(username):
    """ Returns all the raffles that were created by the given user. """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found."}), 404
    return jsonify([r.as_dict() for r in user.raffles])


def _filter_submissions(submissions_list):
    """ Given a submissions list, removes the submissions that were already
    made into raffles. """
    existing_verified_raffles = Raffle.get_verified_raffles()
    excluded_ids = set([r.submission_id for r in existing_verified_raffles])
    return [sub for sub in submissions_list if sub["id"] not in excluded_ids]


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
