from flask import Flask
from app.extensions import db, migrate, rq, limiter, csrf, assets, cache
from app.db import models
from app.routes import base, auth, raffles, api, users
from app.config import ProdConfig
from flask_assets import Bundle


def create_app(config_object=ProdConfig):
    app = Flask('app',
                template_folder='views',
                static_folder='assets')

    app.config.from_object(config_object)

    register_error_handlers(app)
    register_blueprints(app)
    register_extensions(app)

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


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    cache.init_app(app, config=app.config['CACHE_CONFIG'])
    init_and_register_assets(app)
    return None


def init_and_register_assets(app):
    assets.init_app(app)
    js = Bundle('js/util.js', 'js/moment.min.js', 'js/jquery-3.3.1.min.js',
                'js/fontawesome-v5.0.0.min.js', 'js/layouts/header.js',
                'js/layouts/footer.js', filters='jsmin', output='dist/base.js')
    css = Bundle('css/bulma.css', 'css/balloon.min.css', 'css/app.css',
                 filters='cssmin', output='dist/base.css')
    assets.register('js_base', js)
    assets.register('css_base', css)
    return None
