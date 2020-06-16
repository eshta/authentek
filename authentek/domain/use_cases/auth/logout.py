from typing import Tuple

from authentek.database.models import User, BlacklistToken
from authentek.extensions import db


class LogoutUseCase(object):
    def execute(self, auth_token) -> Tuple:
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return response, 200
                except Exception as e:
                    response = {
                        'status': 'fail',
                        'message': e
                    }
                    return response, 200
            else:
                response = {
                    'status': 'fail',
                    'message': resp
                }
                return response, 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response, 403
