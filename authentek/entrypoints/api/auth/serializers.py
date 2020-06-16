from authentek.entrypoints.api import api
from authentek.ext.restplus import custom_fields as fields


login_request = api.model('Login Request', {
    'email': fields.Email(required=True, description="account email"),
    'password': fields.String(required=True, description="account password")
})
