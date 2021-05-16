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
    response.status = HttpStatus.OK

    authorization = environ.get("HTTP_AUTHORIZATION")
    if not jwt_check(authorization):
        response.payload = 'Invalid auth token'
        response.status = HttpStatus.UNAUTHORIZED
        return response

    user_payload = jwt_decode(authorization)

    if user_payload is None:
        response.payload = "Unauthorized"
        response.headers = [ContentType.PLAIN]
        response.status = HttpStatus.UNAUTHORIZED
        return response

    print(user_payload)

    response.payload = dict_to_json(user_payload.__dict__)

    return response

