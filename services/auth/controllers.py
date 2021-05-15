import requests

from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body, dict_to_json


def auth_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.SERVER + "/auth_user", json=body)

    response.payload = res.text
    response.status = HttpStatus.OK

    return response
