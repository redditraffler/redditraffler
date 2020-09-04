from dotenv import load_dotenv
import os

load_dotenv()


def get_boolean_env(env: str, default: bool = False) -> bool:
    return os.getenv(env, default) in [True, "True"]


class BaseConfig:
    TEMPLATE_FOLDER_NAME = os.getenv("TEMPLATE_FOLDER_NAME", "templates")
    STATIC_FOLDER_NAME = os.getenv("STATIC_FOLDER_NAME", "assets")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ENC_KEY = os.getenv("ENC_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    RQ_REDIS_URL = os.getenv("REDIS_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_CONFIG = {
        "CACHE_TYPE": "redis",
        "CACHE_KEY_PREFIX": "redditraffler_",
        "CACHE_REDIS_URL": os.getenv("REDIS_URL"),
        "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24,  # 1 day
    }

    ROLLBAR_ACCESS_TOKEN = os.getenv("ROLLBAR_ACCESS_TOKEN")
    ROLLBAR_ENABLED = False

    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_REDIRECT_URI = os.getenv("REDDIT_REDIRECT_URI")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    REDDIT_AUTH_SCOPES = ["identity", "history", "read"]

    BOT_USERNAME = os.getenv("BOT_USERNAME")
    BOT_PASSWORD = os.getenv("BOT_PASSWORD")
    BOT_CLIENT_ID = os.getenv("BOT_CLIENT_ID")
    BOT_CLIENT_SECRET = os.getenv("BOT_CLIENT_SECRET")

    TALISMAN_CSP = {
        "default-src": "'self'",
        "img-src": [
            "'self' data:",
            "https://az743702.vo.msecnd.net",
            "https://www.google-analytics.com/",
        ],
        "style-src": ["'self' 'unsafe-inline'", "https://use.fontawesome.com/"],
        "font-src": "https://use.fontawesome.com/",
        "connect-src": [
            "'self'",
            "localhost:*",
            "ws://localhost:8080",  # WS for Webpack Dev Server,
            "https://bam.nr-data.net/",
        ],
        "script-src": [
            "'self'",
            "https://www.googletagmanager.com/",
            "https://www.google-analytics.com/ 'unsafe-inline'",
            "https://js-agent.newrelic.com/ 'unsafe-inline'",
            "https://bam.nr-data.net/",
        ],
    }


class DebugConfig(BaseConfig):
    ENV = os.getenv("ENV", "local")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    ROLLBAR_ENABLED = get_boolean_env("ROLLBAR_ENABLED")


class ProdConfig(BaseConfig):
    ENV = os.getenv("ENV", "production")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    ROLLBAR_ENABLED = True


class TestConfig(BaseConfig):
    ENV = "test"
    TESTING = True
    DEBUG = True
    RATELIMIT_ENABLED = False
    WTF_CSRF_ENABLED = False

    CACHE_CONFIG = {"CACHE_TYPE": "null", "CACHE_NO_NULL_WARNING": True}

    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/redditraffler-test.db"

    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = "fakeredis.FakeStrictRedis"
    RQ_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "testId")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "testSecret")
    REDDIT_REDIRECT_URI = os.getenv("REDDIT_REDIRECT_URI", "testRedirectURI")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "testUserAgent")
