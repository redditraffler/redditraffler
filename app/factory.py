from flask import Flask, render_template, url_for
from pprint import pformat
from typing import List
import json
import re

from app.extensions import db, migrate, rq, limiter, csrf, cache, talisman
from app.views import base, auth, raffles, api, users
from app.config import ProdConfig
from app.commands import delete, clear_cache, unescape_submission_titles
from app.logging import configure_logger


def create_app(config_object=ProdConfig) -> Flask:
    app = Flask(
        "app",
        template_folder=config_object.TEMPLATE_FOLDER_NAME,
        static_folder=config_object.STATIC_FOLDER_NAME,
    )
    app.config.from_object(config_object)
    configure_logger(app)

    if app.config["DEBUG_CONFIG"]:
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


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)
    rq.default_result_ttl = 30
    limiter.init_app(app)
    csrf.init_app(app)
    cache.init_app(app, config=app.config["CACHE_CONFIG"])
    talisman.init_app(
        app,
        content_security_policy=app.config["TALISMAN_CSP"],
        force_https=app.config["ENV"] == "production",
    )


def register_commands(app):
    app.cli.add_command(delete)
    app.cli.add_command(clear_cache)
    app.cli.add_command(unescape_submission_titles)


def register_webpack_context_processor(app):
    """Adds the import_webpack_entrypoint utility function in Jinja templates
    """

    def import_webpack_entrypoint(entrypoint: str) -> List[str]:
        """

        Args:
            entrypoint (str): Webpack entrypoint name

        Raises:
            KeyError: If the entrypoint does not exist within the manifest

        Returns:
            List[str]: a HTML string representing script & style tags to import the
            entrypoint's bundled files
        """
        if app.config["TESTING"] or app.config["ENV"] == "test":
            return None

        path_to_manifest = f"{app.static_folder}/dist/manifest.json"

        with open(path_to_manifest, "r") as manifest_file:
            manifest_json = json.load(manifest_file)

        if entrypoint not in manifest_json:
            raise KeyError(f"Entrypoint '{entrypoint}' not found in manifest.json")

        import_tags = []
        for file in manifest_json[entrypoint]:
            path_to_file = url_for("static", filename=f"dist/{file}")
            is_css = re.search(r"\.css$", file)

            if is_css:
                import_tags.append(f'<link rel="stylesheet" href="{path_to_file}" />')
            else:
                import_tags.append(
                    f'<script defer type="text/javascript" src="{path_to_file}">\
                        </script>'
                )

        return "".join(import_tags)

    # Register import_webpack_entrypoint as a context processor
    app.context_processor(
        lambda: dict(import_webpack_entrypoint=import_webpack_entrypoint)
    )
