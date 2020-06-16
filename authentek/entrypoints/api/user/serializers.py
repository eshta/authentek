from authentek.entrypoints.api import api
from authentek.ext.restplus import custom_fields as fields


user_request = api.model('Register Request', {
    'username': fields.String(required=True, description="account username"),
    'email': fields.Email(required=True, description="account email"),
    'password': fields.String(required=True, description="account password")
})
