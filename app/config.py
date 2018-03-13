from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY')
    RQ_REDIS_URL = os.getenv('REDIS_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.getenv('REDIS_URL')
    }

    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
    REDDIT_AUTH_SCOPES = ['identity', 'history', 'read']

    BOT_USERNAME = os.getenv('BOT_USERNAME')
    BOT_PASSWORD = os.getenv('BOT_PASSWORD')
    BOT_CLIENT_ID = os.getenv('BOT_CLIENT_ID')
    BOT_CLIENT_SECRET = os.getenv('BOT_CLIENT_SECRET')


class DevConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    ASSETS_DEBUG = True


class ProdConfig(BaseConfig):
    ENV = os.getenv('ENV') if os.getenv('ENV') else 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class TestConfig(BaseConfig):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/redditraffler-test.db'
    RQ_ASYNC = False
    RATELIMIT_ENABLED = False
    WTF_CSRF_ENABLED = False
