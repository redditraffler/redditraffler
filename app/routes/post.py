from flask import (
    Blueprint,
    redirect,
    url_for,
    session
)

post = Blueprint('post', __name__)


@post.route('/logout', methods=['POST'])
def logout():
    session.clear()
    # Flash message
    return redirect(url_for('get.index'))
