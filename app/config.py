from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
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


class DebugConfig(BaseConfig):
    ENV = os.getenv("ENV", "local")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    ASSETS_DEBUG = True
    ROLLBAR_ENABLED = os.getenv("ENV", False)


class ProdConfig(BaseConfig):
    ENV = os.getenv("ENV", "production")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    ROLLBAR_ENABLED = True


class TestConfig(BaseConfig):
    ENV = "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/redditraffler-test.db"
    RQ_ASYNC = False
    RATELIMIT_ENABLED = False
    WTF_CSRF_ENABLED = False
    CACHE_CONFIG = {"CACHE_TYPE": "null", "CACHE_NO_NULL_WARNING": True}
