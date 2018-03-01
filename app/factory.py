from flask import Flask
from app.db import db, migrate, models
from app.jobs import rq
from app.routes import base, auth, raffles, api, users
import app.config as config


def create_app():
    app = Flask(__name__,
                template_folder='views',
                static_folder='assets')

    app.config.from_object(config)

    register_error_handlers(app)
    register_blueprints(app)

    db.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)

    return app


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


def register_blueprints(app):
    app.register_blueprint(base.base)
    app.register_blueprint(auth.auth, url_prefix='/auth')
    app.register_blueprint(raffles.raffles, url_prefix='/raffles')
    app.register_blueprint(api.api, url_prefix='/api')
    app.register_blueprint(users.users, url_prefix='/users')
    return None
