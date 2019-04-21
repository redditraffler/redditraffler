# To start the server:
# $ export FLASK_APP=runserver.py
# $ flask run

from flask.helpers import get_debug_flag
from app.config import DebugConfig, ProdConfig
from app.factory import create_app

cfg = DebugConfig if get_debug_flag() else ProdConfig
app = create_app(cfg)
