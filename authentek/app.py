from flask import Flask, Blueprint

from authentek.entrypoints.api import api
from authentek.extensions import db, migrate, bcrypt, cors
from authentek.entrypoints.api.user.endpoints import ns as users_namespace
from authentek.entrypoints.api.auth.endpoints import ns as auth_namespace
import os


def create_app(testing=False, cli=False) -> Flask:
    """Application factory, used to create application
    """
    from authentek.internal import app
    app.config.from_object(os.getenv('APP_SETTINGS', 'authentek.server.config.DevelopmentConfig'))
    if testing is True:
        app.config["TESTING"] = True

    app = configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_extensions(flask_app, cli):
    """configure flask extensions
        """
    db.init_app(flask_app)

    cors.init_app(flask_app)
    db.app = flask_app

    bcrypt.init_app(flask_app)
    if cli is True:
        migrate.init_app(flask_app, db)
    return flask_app


def register_blueprints(flask_app):
    """register all blueprints for application
    """
    blueprint = Blueprint('api', __name__, url_prefix='/v1')
    api.init_app(blueprint)
    api.add_namespace(users_namespace)
    api.add_namespace(auth_namespace)
    if blueprint.name not in flask_app.blueprints.keys():
        flask_app.register_blueprint(blueprint)
    else:
        flask_app.blueprints[blueprint.name] = blueprint


if __name__ == '__main__':
    app = create_app(False, True)
    app.run(host='0.0.0.0', port=8888)
