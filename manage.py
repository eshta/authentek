# manage.py


import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy


from authentek import settings
from authentek.app import initialize_app, log, main
from authentek.internal import app
from authentek import settings
from authentek.extensions import db
from authentek.database.models import User, BlacklistToken  # noqa

app.config.from_object(settings)
manager = Manager(app)
initialize_app(app, True)


COV = coverage.coverage(
    branch=True,
    include='authentek/*',
    omit=[
        'authentek/tests/*',
    ]
)
COV.start()

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('authentek/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('authentek/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def migrate():
    print(app.extensions)

    # migrations
    manager.add_command('db', MigrateCommand)

@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()
