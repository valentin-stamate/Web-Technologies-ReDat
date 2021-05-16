import requests

from services.auth.jwt_util import jwt_check, jwt_decode
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body, dict_to_json
from util.validation.validation import valid_username, valid_password


def auth_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    if not valid_username(body['username']) or not valid_password(body['password']):
        response.payload = "Invalid user or password"
        response.headers = [ContentType.TEXT]
        response.status = HttpStatus.BAD_REQUEST
        return response

    res = requests.post(ServiceUrl.SERVER + "/auth_user", json=body)

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def check_user_auth(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    authorization = environ.get("HTTP_AUTHORIZATION")
    if not jwt_check(authorization):
        response.payload = 'Invalid auth token'
        response.status = HttpStatus.UNAUTHORIZED
        return response

    response.payload = dict_to_json(jwt_decode(authorization).__dict__)
    response.status = HttpStatus.OK

    return response

