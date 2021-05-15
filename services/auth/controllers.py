import requests

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
