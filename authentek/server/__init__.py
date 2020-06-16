# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from authentek.server.auth.views import auth_blueprint

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'authentek.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
app.register_blueprint(auth_blueprint)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
