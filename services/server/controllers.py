import json

from services.auth.jwt_util import jwt_encode
from services.server.database.models.user_model import UserModel
from services.server.renderer import render_file
from util.instance.user_jwt_data import UserJWTData
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.util import read_body, json_to_dict, dict_to_json


def get_file(path):
    response = ResponseData()

    response.payload = render_file(path)
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def auth_user(environ):
    response = ResponseData()
    response.headers = [ContentType.JSON]

    response_body = json_to_dict(read_body(environ))

    user = UserModel(username=response_body['username'], password=response_body['password'])

    status = user.login()

    if not status['status']:
        response.payload = status['message']
        response.status = HttpStatus.BAD_REQUEST
        return response

    user_data = UserJWTData(user_id=user.user_id, username=user.username, email=user.email)
    token = jwt_encode(user_data)

    response.payload = dict_to_json({'token': token})
    response.status = HttpStatus.OK

    return response

