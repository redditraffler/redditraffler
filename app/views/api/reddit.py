from flask import abort, jsonify, request, url_for

from app.services import reddit_service
from app.db.models.raffle import Raffle


def get_reddit_submission():
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


RouteConfigs = [{"rule": "/submission", "view_func": get_reddit_submission}]

