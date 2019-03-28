from flask import abort, Blueprint, redirect, render_template, request, session, url_for
from app.util import reddit

base = Blueprint("base", __name__)


@base.route("/")
def index():
    return render_template(
        "base/index.html",
        title="the raffle system for reddit submissions",
        reddit_login_url=reddit.get_auth_url(),
    )


@base.route("/about")
def about():
    return render_template("base/about.html", title="About")


@base.route("/faq")
def faq():
    return render_template("base/faq.html", title="Frequently Asked Questions")


@base.route("/terms-of-service")
def tos():
    return render_template("base/terms-of-service.html", title="Terms of Service")


@base.route("/privacy-policy")
def privacy_policy():
    return render_template("base/privacy-policy.html", title="Privacy Policy")
