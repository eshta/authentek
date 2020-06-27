import logging
from typing import Any

from flask import request, make_response, jsonify
from flask_restx import Resource

from authentek.domain.use_cases.auth.login import LoginUseCase
from authentek.domain.use_cases.auth.logout import LogoutUseCase
from authentek.domain.use_cases.auth.status import StatusUseCase
from authentek.entrypoints.api.auth.serializers import login_request
from authentek.entrypoints.api import api

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='Authentication')


@ns.route('/login', strict_slashes=False)
class Login(Resource):
    @api.expect(login_request)
    def post(self) -> Any:
        """
            Authenticates the user
        """
        data = request.json
        use_case = LoginUseCase()

        response = use_case.execute(data)
        return make_response((jsonify(response[0]), response[1]))


@ns.route('/logout', strict_slashes=False)
class Logout(Resource):
    @api.expect()
    def post(self) -> Any:
        """
            Logs out the user
        """
        use_case = LogoutUseCase()
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        response = use_case.execute(auth_token)
        return make_response((jsonify(response[0]), response[1]))


@api.header('Authorization', 'Authorization header (Bearer token)')
@ns.route('/info', strict_slashes=False)
class Info(Resource):
    def get(self):
        # get auth token
        auth_header = request.headers.get('authorization')
        if auth_header:
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''
        use_case = StatusUseCase()
        response = use_case.execute(auth_token)
        return make_response((jsonify(response[0]), response[1]))
