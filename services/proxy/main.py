import requests

from services.proxy.controllers import get_page, get_static_resource, auth_token
from util.pages import paths
from util.request.response_data import HttpStatus, ContentType
from util.response_data import ResponseData
# CONTROLLER HANDLER
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    print(path)
    if path in paths:
        response = get_page(environ)
    elif path.startswith('/static'):
        response = get_static_resource(environ)
    elif path == "/auth_user":
        response = auth_token(environ)
    elif path == '/register_user':
        res = requests.post(ServiceUrl.AUTH + "/register_user", json=json_to_dict(read_body(environ)))
        response.payload = res.text
    elif path == '/update_user':
        body = json_to_dict(read_body(environ))
        res = requests.post(ServiceUrl.AUTH + "/update_user",
                            headers={'Authorization': environ.get("HTTP_AUTHORIZATION")},
                            json=body)
        user_data = json_to_dict(res.text)
        body['id'] = user_data['user_id']
        if str(res.status_code) == HttpStatus.OK:
            res = requests.post(ServiceUrl.SERVER + "/update_user", json=body)
            response.payload = res.text
    else:
        response.status = HttpStatus.NOT_FOUND
        response.payload = "Page not found."
        response.headers = [ContentType.HTML]

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response_headers
    )

    return iter([response.payload])
