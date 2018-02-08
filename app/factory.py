from flask import Flask
from app.routes.get import get


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
    register_error_handlers(app)

    app.register_blueprint(get)
    return app
