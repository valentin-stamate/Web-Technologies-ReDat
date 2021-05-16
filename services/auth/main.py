# CONTROLLER HANDLER
import requests

from services.auth.controllers import auth_user, check_user_auth
from services.auth.jwt_util import jwt_check, jwt_decode
from services.server.database.models import user_model
from util.request.response_data import HttpStatus, ContentType
from util.response_data import ResponseData
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body, dict_to_json


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    response.headers = [ContentType.JSON]
    if path == "":
        response.payload = "Hello there. This is the auth service."
    elif path == "/auth_user":
        response = auth_user(environ)
    elif path == "/register_user":
        res = requests.post(ServiceUrl.SERVER + "/register_user", json=json_to_dict(read_body(environ)))
        response.payload = res.text
    elif path == '/check_user_auth':
        response = check_user_auth(environ)

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response_headers
    )

    return iter([response.payload])


# REGISTER NEW USER
def register(environ) -> dict:
    body_dict = json_to_dict(read_body(environ))

    db_user = user_model.UserModel.get_by_username(body_dict['username'])['object']

    if db_user is not None:
        return {'status': False, 'message': "Username already exists"}

    new_user = user_model.UserModel(body_dict['username'], body_dict['firstname'], body_dict['lastname'],
                                    body_dict['email'],
                                    body_dict['password'])
    if not new_user.is_valid()['status']:
        return {'status': False, 'message': new_user.is_valid()['message']}
    res = requests.post(ServiceUrl.SERVER + "/register_user", json=body_dict)
    return {'status': True, 'message': "User created"}
