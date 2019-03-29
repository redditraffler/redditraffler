from flask import abort, Blueprint, jsonify, redirect, request, session, url_for
from sqlalchemy.orm import load_only
from app.util import reddit
from app.util.raffle_form_validator import RaffleFormValidator
from app.extensions import rq
from app.db.models import Raffle, User
from app.jobs.raffle_job import raffle


api = Blueprint("api", __name__)


@api.route("/submissions")
def submissions():
    """ Return the user's Reddit submissions that are not already made
    into raffles. """
    if "reddit_refresh_token" not in session:
        abort(401)

    submissions = reddit.get_user_submissions(session["reddit_refresh_token"])
    return jsonify(_filter_submissions(submissions) if submissions else None)


@api.route("/submission")
def submission():
    """ Accepts a `url` parameter and returns the associated submission. If
    a raffle exists for the given submission then the path to that raffle is
    returned. """
    if not request.args.get("url"):
        abort(400)

    url = request.args.get("url")
    sub_id = reddit.submission_id_from_url(url)

    if Raffle.query.filter_by(submission_id=sub_id).scalar():
        return jsonify({"url": url_for("raffles.show", submission_id=sub_id)}), 303
    else:
        submission = reddit.get_submission(sub_url=url)
        return jsonify(submission) if submission else abort(404)


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
    form = request.form.to_dict()
    validator = RaffleFormValidator(form)
    if not validator.run():
        return jsonify({"message": "Form validation failed."}), 422
    form = validator.get_sanitized_form()
    user = _try_get_user_from_session()
    sub_id = reddit.submission_id_from_url(form["submissionUrl"])
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
    existing_verified_raffles = (
        Raffle.query.filter(Raffle.user_id != None)
        .options(load_only("submission_id"))
        .all()
    )
    excluded_ids = set([r.submission_id for r in existing_verified_raffles])
    return [sub for sub in submissions_list if sub["id"] not in excluded_ids]


def _try_get_user_from_session():
    if "reddit_username" in session:
        return User.query.filter_by(username=session["reddit_username"]).first()
    else:
        return None


def _raffle_params_from_form(form):
    return {
        "submission_url": form["submissionUrl"],
        "winner_count": form["winnerCount"],
        "min_account_age": form["minAge"],
        "min_comment_karma": form["minComment"],
        "min_link_karma": form["minLink"],
        "ignored_users": form["ignoredUsers"],
    }
