from flask import abort, Blueprint, render_template, request, Markup
from app.util import reddit
from app.db.models import User, Raffle
from app.extensions import rq, cache, db

raffles = Blueprint("raffles", __name__)


@raffles.route("")
def index():
    raffles = Raffle.query.all()
    return render_template(
        "raffles/index.html", title="View All Raffles", raffles=raffles
    )


@raffles.route("/new")
def new():
    return render_template(
        "raffles/new.html", title="New Raffle", reddit_login_url=reddit.get_auth_url()
    )


@raffles.route("/<job_id>/status")
def status(job_id):
    if not rq.get_queue().fetch_job(job_id):
        abort(404)
    return render_template("raffles/status.html", title="Raffle Status", job_id=job_id)


@raffles.route("/<submission_id>")
def show(submission_id):
    raffle = _raffle_from_cache(submission_id)
    if not raffle:
        abort(404)
    title = Markup('Results For "%s"' % raffle.submission_title)
    return render_template("raffles/show.html", title=title, raffle=raffle)


def _raffle_from_cache(sub_id):
    cache_key = "raffle_{}".format(sub_id)
    cached = cache.get(cache_key)
    if not cached:
        raffle = Raffle.query.filter_by(submission_id=sub_id).first()
        if raffle:
            cache.set(cache_key, raffle)
    else:
        db.session.add(cached)
        raffle = cached
    return raffle
