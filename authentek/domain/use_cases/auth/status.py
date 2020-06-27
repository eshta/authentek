from typing import Tuple

from authentek.database.models import User


class StatusUseCase(object):
    def execute(self, auth_token) -> Tuple:
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, int):
                user = User.query.filter_by(id=resp).first()
                response = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'admin': user.admin,
                        'uuid': user.uuid,
                        'registered_on': user.registered_on
                    }
                }

                return response, 200
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
            return response, 401
