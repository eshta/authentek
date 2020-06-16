from typing import Tuple

from authentek.database.models import User
from authentek.extensions import bcrypt
from authentek.logger import log


class LoginUseCase(object):
    def execute(self, command) -> Tuple:
        try:
            user = User.query.filter_by(
                email=command.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                    user.password, command.get('password')
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return response, 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return response, 404
        except Exception as e:
            log.exception(e)
            response = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response, 500
