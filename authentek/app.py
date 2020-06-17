import os

from flask import Blueprint

from authentek import settings
from authentek.entrypoints.api.user.endpoints import ns as users_namespace
from authentek.entrypoints.api.auth.endpoints import ns as auth_namespace
from authentek.entrypoints.api import api
from authentek.extensions import db, migrate, bcrypt
from authentek.internal import app
from authentek.logger import log


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def configure_app(flask_app):
    flask_app.config.from_object(os.getenv('APP_SETTINGS', 'authentek.server.config.DevelopmentConfig'))
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

    flask_app.config['ENV'] = settings.ENV
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP



def configure_extensions(flask_app, cli):
    """configure flask extensions
    """
    db.init_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/v1')
    api.init_app(blueprint)
    api.add_namespace(users_namespace)
    api.add_namespace(auth_namespace)
    if blueprint.name not in flask_app.blueprints.keys():
        flask_app.register_blueprint(blueprint)
    else:
        flask_app.blueprints[blueprint.name] = blueprint

    db.app = flask_app
    db.create_all()

    bcrypt.init_app(flask_app)
    if cli is True:
        migrate.init_app(flask_app, db)

def initialize_app(flask_app, cli=False):
    configure_app(flask_app)
    configure_extensions(flask_app, cli)

    # db.init_app(flask_app)
    # configure_extensions(flask_app, cli)

    print(flask_app.blueprints)


def main():
    from authentek.database.models import User, BlacklistToken  # noqa
    initialize_app(app)
    log.info(str(app.config))
    log.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))

    @app.route("/links")
    def links():
        from flask import url_for
        links = []
        for rule in app.url_map.iter_rules():
            if len(rule.defaults) >= len(rule.arguments):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))

        return links
    return app


def run():
    app.run(host='0.0.0.0', port=8888, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    flask_app = main()
    flask_app.run()
