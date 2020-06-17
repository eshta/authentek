from flask import jsonify

from authentek.database import db
from authentek.database.models import Post, Category, User
from authentek.logger import log

def login():
    from authentek.server import bcrypt
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response)), 200
        else:
            response = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(response)), 404
    except Exception as e:
        print(e)
        response = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(response)), 500


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

