import rollbar
import logging

from rollbar.logger import RollbarHandler


def configure_logger(app):
    log_level = _get_log_level_from_config(app)
    _configure_main_logger(app, log_level)
    _configure_rollbar(app, log_level)


def _get_log_level_from_config(app):
    level = app.config.get("LOG_LEVEL", "INFO")
    try:
        return getattr(logging, level)
    except:
        return logging.INFO


def _configure_main_logger(app, log_level):
    app.logger.setLevel(log_level)


def _configure_rollbar(app, log_level):
    try:
        env = app.config["ENV"]
        enabled = app.config["ROLLBAR_ENABLED"]
        api_token = app.config["ROLLBAR_ACCESS_TOKEN"]
    except KeyError:
        raise KeyError("Could not get Rollbar config from app config object")

    rollbar.init(
        api_token,
        env,
        handler="blocking",
        enabled=enabled,
        allow_logging_basic_config=False,
    )

    rollbar_handler = RollbarHandler(history_size=5)
    rollbar_handler.setLevel(log_level)

    app.logger.addHandler(rollbar_handler)
