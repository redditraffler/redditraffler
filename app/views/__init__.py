from .oauth import oauth


def init_views(app):
    app.register_blueprint(oauth, url_prefix="/oauth")
