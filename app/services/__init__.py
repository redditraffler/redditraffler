from .reddit_service import RedditService

reddit_service = RedditService()


def init_services(app):
    reddit_service.init_app(app)
