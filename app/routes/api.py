from flask import Blueprint, session, jsonify, abort, request, url_for
from app.util import reddit
from app.extensions import rq
from app.db.models import Raffle


api = Blueprint('api', __name__)


@api.route('/submissions')
def submissions():
    """ Return the user's Reddit submissions, filtering out submissions
    that have already been made into raffles. """

    if 'reddit_refresh_token' not in session:
        abort(401)

    submissions = reddit.get_user_submissions(session['reddit_refresh_token'])
    return jsonify(_filter_submissions(submissions) if submissions else None)


@api.route('/submission')
def submission():
    """ Accepts a `url` parameter and returns the associated submission. If
    a raffle exists for the given submission then the path to that raffle is
    returned. """

    if not request.args.get('url'):
        abort(400)

    url = request.args.get('url')
    sub_id = reddit.submission_id_from_url(url)

    if Raffle.query.filter_by(submission_id=sub_id).scalar():
        return jsonify({
            'url': url_for('raffles.show', submission_id=sub_id)
        }), 303
    else:
        submission = reddit.get_submission(sub_url=url)
        return jsonify(submission) if submission else abort(404)


@api.route('/job_status')
def status():
    job = rq.get_queue().fetch_job(request.args.get('job_id'))
    if not job:
        abort(404)

    status = job.meta.get('status') if 'status' in job.meta \
        else 'Waiting to process...'

    return jsonify({'status': status, 'error': job.meta.get('error')})


def _filter_submissions(submissions_list):
    existing_raffle_ids = [tuple[0] for tuple in Raffle.query.
                           with_entities(Raffle.submission_id).all()]
    return [sub for sub in submissions_list if
            sub['id'] not in existing_raffle_ids]
