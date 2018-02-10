from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from app.lib import reddit

raffle = Blueprint('raffle', __name__)


@raffle.route('/create')
def create():
    return render_template('raffle/create.html')
