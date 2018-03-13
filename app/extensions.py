from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment
from flask_caching import Cache
from app.config import BaseConfig

db = SQLAlchemy()
migrate = Migrate(directory='app/db/migrations')
rq = RQ()
limiter = Limiter(key_func=get_remote_address, default_limits=['2 per second'])
csrf = CSRFProtect()
assets = Environment()
cache = Cache(config=BaseConfig.CACHE_CONFIG)
