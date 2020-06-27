import logging

from flask import request, make_response, jsonify
from flask_restx import Resource

from authentek.entrypoints.api.restplus import api
from authentek.entrypoints.api.user.business import create_user, view_user
from authentek.entrypoints.api.user.serializers import user_request
from authentek.logger import log

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Users')


@ns.route('/', strict_slashes=False)
class UsersCollection(Resource):
    @api.doc(responses={
        201: 'Created',
        400: 'Bad Request',
        500: 'Internal Server Error',
    })
    @api.expect(user_request)
    def post(self):
        """
            Creates a user
        """
        data = request.json
        response = create_user(data)
        try:
            log.exception(response)
            return make_response((jsonify(response[0]), response[1]))
        except Exception as e:
            log.exception(e)
            return make_response(jsonify({
                'status': 'fail',
                'message': 'Service is unavailable.'
            }), 500)

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        500: 'Internal Server Error'
    })
    @api.header('Authorization', 'Authorization header (Bearer token)')
    def get(self):
        # get auth token
        auth_header = request.headers.get('authorization')
        if auth_header:
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''

        if auth_token:
            response = view_user(auth_token)
            try:
                return make_response((jsonify(response[0]), response[1]))
            except Exception as e:
                log.exception(e)
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response)), 401
