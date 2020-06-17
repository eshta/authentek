# project/server/__init__.py

import os

from flask import Flask

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'authentek.server.config.DevelopmentConfig'
)
