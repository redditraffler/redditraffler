from enum import Enum
from flask import request
import rollbar
import inspect


def get_caller_name():
    frame_info = inspect.stack()[2]
    module = inspect.getmodule(frame_info.frame)
    fn = frame_info.function
    return f"{module.__name__}.{fn}"


class LogLevel(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class RollbarService:
    def init_app(self, app):
        env = app.config.get("ENV", "development")
        enabled = app.config.get("ROLLBAR_ENABLED", False)
        api_token = app.config.get("ROLLBAR_ACCESS_TOKEN")

        rollbar.init(api_token, env, enabled=enabled, allow_logging_basic_config=False)

    def exception(self, context={}, level=LogLevel.ERROR.value):
        context.update({"source": get_caller_name()})
        rollbar.report_exc_info(
            request=request, extra_data={"context": context}, level=level
        )

    def critical(self, message, context={}):
        source = get_caller_name()
        rollbar.report_message(
            f"[{source}] {message}",
            level=LogLevel.CRITICAL.value,
            request=request,
            extra_data={"context": context},
        )

    def error(self, message, context={}):
        source = get_caller_name()
        rollbar.report_message(
            f"[{source}] {message}",
            level=LogLevel.ERROR.value,
            request=request,
            extra_data={"context": context},
        )

    def warn(self, message, context={}):
        source = get_caller_name()
        rollbar.report_message(
            f"[{source}] {message}",
            level=LogLevel.WARNING.value,
            request=request,
            extra_data={"context": context},
        )

    def info(self, message, context={}):
        source = get_caller_name()
        rollbar.report_message(
            f"[{source}] {message}",
            level=LogLevel.INFO.value,
            request=request,
            extra_data={"context": context},
        )

    def debug(self, message, context={}):
        source = get_caller_name()
        rollbar.report_message(
            f"[{source}] {message}",
            level=LogLevel.DEBUG.value,
            request=request,
            extra_data={"context": context},
        )
