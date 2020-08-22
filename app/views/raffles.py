from flask import abort, Blueprint, render_template, Markup
from app.services import reddit_service
from app.extensions import rq, db
from app.db.models.raffle import Raffle

raffles = Blueprint("raffles", __name__)


@raffles.route("/new")
def new():
    return render_template(
        "raffles/new.html",
        title="New Raffle",
        reddit_login_url=reddit_service.get_oauth_url(),
    )


@raffles.route("/<job_id>/status")
def status(job_id):
    if not rq.get_queue().fetch_job(job_id):
        abort(404)
    return render_template("raffles/status.html", title="Raffle Status", job_id=job_id)


@raffles.route("/<submission_id>")
def show(submission_id):
    raffle = Raffle.query.filter_by(submission_id=submission_id).first()
    if not raffle:
        abort(404)

    title = Markup('Results For "%s"' % raffle.submission_title)
    return render_template("raffles/show.html", title=title, raffle=raffle)
