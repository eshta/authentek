# project/server/tests/base.py
import time

from flask_testing import TestCase

from authentek.app import main
from authentek.database import db


class BaseTestCase(TestCase):
    """ Base Tests """

    def get_timestamp(self):
        return str(time.time()).replace('.', '_')

    def create_app(self):
        from authentek.internal import app
        app.config.from_object('authentek.server.config.TestingConfig')
        app = main()
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
