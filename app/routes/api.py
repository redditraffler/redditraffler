from flask import Blueprint, session, jsonify, abort
from app.util import reddit

api = Blueprint('api', __name__)


@api.route('/submissions')
def submissions():
    """ Return the user's Reddit submissions. """

    if 'reddit_refresh_token' not in session:
        abort(401)

    submissions = reddit.get_user_submissions(session['reddit_refresh_token'])
    return jsonify(submissions)
