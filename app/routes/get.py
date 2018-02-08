from flask import Blueprint, render_template

get = Blueprint('get', __name__)


@get.route('/')
def index():
    return render_template('index.html', title='Home')
