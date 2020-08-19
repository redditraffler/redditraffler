from flask import Blueprint

from .jobs import RouteConfigs as JobsRouteConfigs
from .users import RouteConfigs as UsersRouteConfigs
from .reddit import RouteConfigs as RedditRouteConfigs
from .raffles import RouteConfigs as RafflesRouteConfigs


api = Blueprint("api", __name__)

# Import the routes and register them to this blueprint.
# Each route_config should be a dict of add_url_rule()'s params
# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.add_url_rule
for route_config in [
    *JobsRouteConfigs,
    *UsersRouteConfigs,
    *RedditRouteConfigs,
    *RafflesRouteConfigs,
]:
    api.add_url_rule(**route_config)
