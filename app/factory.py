from flask import Flask
from app.routes.base import base
from app.routes.auth import auth
from app.routes.raffles import raffles
from app.routes.api import api
from app.db import db

import app.config as config


def register_error_handlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        return 'unauthorized', 401

    @app.errorhandler(404)
    def not_found(error):
        return 'not found', 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return 'internal server error', 500


def create_app():
    app = Flask(__name__,
                template_folder='views',
                static_folder='assets')

    app.config.from_object(config)

    register_error_handlers(app)

    app.register_blueprint(base)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(raffles, url_prefix='/raffles')
    app.register_blueprint(api, url_prefix='/api')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
