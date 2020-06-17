from flask import jsonify
from sqlalchemy.exc import IntegrityError

from authentek.database import db
from authentek.database.models import User
from authentek.logger import log


def create_user(data):
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        try:
            user = User(
                email=data.get('email'),
                password=data.get('password'),
                username=data.get('username')
            )

            # insert user
            db.session.add(user)
            db.session.commit()

            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }
            return response, 201
        except TypeError:
            response = {
                'status': 'fail',
                'message': 'Some error occured. Please try again later!'
            }
            log.exception(e)
            return response, 500
        except IntegrityError as e:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response, 400
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Some error occured. Please try again later!'
            }
            log.exception(e)
            return response, 500
    else:
        response = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response, 400


def view_user(auth_token):
    resp = User.decode_auth_token(auth_token)
    if isinstance(resp, int):
        user = User.query.filter_by(id=resp).first()
        response = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on
            }
        }

        return response, 200
    response = {
        'status': 'fail',
        'message': resp
    }
    return response, 401
