import unittest

from authentek.database.models import User
from authentek.extensions import db
from authentek.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test_{}@test.com'.format(self.get_timestamp()),
            username='test_{}'.format(self.get_timestamp()),
            password='test',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = User(
            email='test_{}@test.com'.format(self.get_timestamp()),
            username='test_{}'.format(self.get_timestamp()),
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)


if __name__ == 'main':
    unittest.main()
