from flask import Flask, render_template, url_for
from flask_assets import Bundle
from pprint import pformat
import json

from app.extensions import db, migrate, rq, limiter, csrf, assets, cache
from app.routes import base, auth, raffles, api, users
from app.config import ProdConfig
from app.commands import delete, clear_cache
from app.logging import configure_logger
from app.views import oauth as oauth_view, users as users_view


def create_app(config_object=ProdConfig):
    app = Flask("app", template_folder="views", static_folder="assets")
    app.config.from_object(config_object)
    configure_logger(app)
    app.logger.debug(pformat(app.config))
    register_error_handlers(app)
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_webpack_context_processor(app)
    return app


def register_error_handlers(app):
    def render_error(error):
        code_msg = {
            401: "Unauthorized",
            404: "Not Found",
            422: "Unprocessable Entity",
            500: "Internal Server Error",
        }
        error_code = getattr(error, "code", 500)
        return (
            render_template(
                "base/error.html",
                title="Error {}".format(error_code),
                code=error_code,
                code_msg=code_msg.get(error_code),
            ),
            error_code,
        )

    for code in [401, 404, 500]:
        app.errorhandler(code)(render_error)


def register_blueprints(app):
    app.register_blueprint(base.base)
    app.register_blueprint(auth.auth, url_prefix="/auth")
    app.register_blueprint(raffles.raffles, url_prefix="/raffles")
    app.register_blueprint(api.api, url_prefix="/api")
    app.register_blueprint(users.users, url_prefix="/users")

    # JSON API
    app.register_blueprint(oauth_view.oauth, url_prefix="/api/oauth")
    app.register_blueprint(users_view.user, url_prefix="/api/users")


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)
    rq.default_result_ttl = 30
    limiter.init_app(app)
    csrf.init_app(app)
    cache.init_app(app, config=app.config["CACHE_CONFIG"])
    init_ssl(app)
    init_and_register_assets(app)


def init_and_register_assets(app):
    assets.init_app(app)
    js = Bundle(
        "js/util.js",
        "js/moment.min.js",
        "js/jquery-3.3.1.min.js",
        "js/fontawesome-v5.0.0.min.js",
        "js/sweetalert2.min.js",
        "js/layouts/header.js",
        "js/layouts/footer.js",
        filters="jsmin",
        output="dist/base.js",
    )
    css = Bundle(
        "css/bulma.css",
        "css/balloon.min.css",
        "css/app.css",
        filters="cssmin",
        output="dist/base.css",
    )
    assets.register("js_base", js)
    assets.register("css_base", css)


def init_ssl(app):
    # Workaround because Flask-SSLify doesn't support app factories
    if app.config["ENV"] == "production":
        from flask_sslify import SSLify

        SSLify(app)


def register_commands(app):
    app.cli.add_command(delete)
    app.cli.add_command(clear_cache)


def register_webpack_context_processor(app):
    """Adds the url_for_webpack_output utility function in Jinja templates
    """

    def url_for_webpack_output(entrypoint: str):
        """

        Args:
            entrypoint (str): Webpack entrypoint name

        Raises:
            KeyError: If the entrypoint does not exist within the manifest

        Returns:
            str: the path to the target file within the app's static folder
        """
        path_to_manifest = f"{app.static_folder}/manifest.json"
        entrypoint_file_name = f"{entrypoint}.js"

        with open(path_to_manifest, "r") as manifest_file:
            manifest_json = json.load(open(path_to_manifest, "r"))

        if entrypoint_file_name not in manifest_json:
            raise KeyError(
                f"Entrypoint '{entrypoint_file_name}' not found in manifest.json"
            )

        return url_for("static", filename=manifest_json[entrypoint_file_name])

    # Register url_for_webpack_output as a context processor
    app.context_processor(lambda: dict(url_for_webpack_output=url_for_webpack_output))
