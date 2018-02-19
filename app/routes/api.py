from flask import Blueprint, session, jsonify, abort, request
from app.util import reddit

api = Blueprint('api', __name__)


@api.route('/submissions')
def submissions():
    """ Return the user's Reddit submissions. """

    if 'reddit_refresh_token' not in session:
        abort(401)

    submissions = reddit.get_user_submissions(session['reddit_refresh_token'])
    return jsonify(submissions)


@api.route('/submission')
def submission():
    """ Accepts a `url` or `id` parameter and returns the associated
    submission. """

    if not (request.args.get('url') or request.args.get('id')):
        abort(400)

    if request.args.get('url'):
        submission = reddit.get_submission(sub_url=request.args.get('url'))
    else:
        submission = reddit.get_submission(sub_id=request.args.get('id'))

    return jsonify(submission) if submission else abort(404)
