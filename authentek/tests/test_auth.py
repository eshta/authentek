import json
import time
import unittest

from authentek.database.models import User, BlacklistToken
from authentek.extensions import db
from authentek.logger import log
from authentek.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def register_user(self, username, email, password):
        return self.client.post(
            '/v1/users/',
            data=json.dumps(dict(
                email=email,
                password=password,
                username=username
            )),
            content_type='application/json',
        )

    def register_random_user(self):
        email = 'joe_{}@gmail.com'.format(self.get_timestamp())
        username = 'joe_{}'.format(self.get_timestamp())
        password = '123456'
        self.register_user(username, email, password)

        return User(username=username, password=password, email=email)


    def test_registration(self):
        with self.client:
            response = self.register_user('joe_{}'.format(self.get_timestamp()),
                                          'joe_{}@gmail.com'.format(self.get_timestamp()), '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = self.register_random_user()
        with self.client:
            response = self.client.post(
                '/v1/users/',
                data=json.dumps(dict(
                    email=user.email,
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.register_user('joe_{}'.format(self.get_timestamp()),
                                               'joe_{}@gmail.com'.format(self.get_timestamp()), '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.register_user('joe_{}'.format(self.get_timestamp()),
                                          'joe_{}@gmail.com'.format(self.get_timestamp()), '123456')

            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            resp_register = self.register_user('joe_{}'.format(self.get_timestamp()),
                                               'joe_{}@gmail.com'.format(self.get_timestamp()), '123456')
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertTrue(data['data']['admin'] is 'true' or 'false')

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            user = self.register_random_user()
            # user login
            resp_login = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    email=user.email,
                    password='123456'
                )),
                content_type='application/json'
            )
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            user = self.register_random_user()
            # user login
            resp_login = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    email=user.email,
                    password='123456'
                )),
                content_type='application/json'
            )
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            # invalid token logout
            time.sleep(6)
            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'], 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            email = 'joe_{}@gmail.com'.format(self.get_timestamp())
            username = 'joe_{}'.format(self.get_timestamp())
            resp_register = self.register_user(username=username, email=email, password='123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=email,
                    password='123456'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(data['message'], 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """ Test for user status with a blacklisted valid token """
        with self.client:
            resp_register = self.register_user('joe_{}'.format(self.get_timestamp()),
                                               'joe_{}@gmail.com'.format(self.get_timestamp()), '123456')
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/v1/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(data['message'], 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == 'main':
    unittest.main()
