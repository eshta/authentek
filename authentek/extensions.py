"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS(resources={r"/v1/*": {"origins": "*"}})
