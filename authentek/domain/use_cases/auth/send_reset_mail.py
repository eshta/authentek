from typing import Tuple

from authentek.database.models import User


class SendResetMailUseCase(object):
    def execute(self, command) -> Tuple:
        user = User.query.filter_by(
            email=command.get('email')
        ).first()
        if user:
            hash = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))
        else:
            response = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return response, 404
