import requests

from services.auth.jwt_util import jwt_check, jwt_decode, jwt_encode
from util.instance.user_jwt_data import UserJWTData
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from secrets import ServiceUrl
from util.util import json_to_dict, read_body, dict_to_json


def auth_user(environ):
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.SERVER + "/check_user", json=body)

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    body = json_to_dict(res.text)

    user_data = UserJWTData(user_id=body['user_id'], username=body['username'], email=body['email'])
    token = jwt_encode(user_data)

    response.payload = dict_to_json({'token': token})
    response.status = HttpStatus.OK

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

    response.payload = dict_to_json(user_payload.__dict__)

    return response


def register_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    res = requests.post(ServiceUrl.SERVER + "/register_user", json=json_to_dict(read_body(environ)))

    response.payload = res.text
    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        return response

    body = json_to_dict(res.text)

    user_data = UserJWTData(user_id=body['user_id'], username=body['username'], email=body['email'])
    token = jwt_encode(user_data)

    response.payload = dict_to_json({'token': token})
    response.status = HttpStatus.OK

    return response

