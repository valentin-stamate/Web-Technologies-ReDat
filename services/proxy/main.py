import requests

from services.proxy.controllers import get_page, get_static_resource
from util.pages import paths
from util.request.response_data import HttpStatus, ContentType
from util.response_data import ResponseData
from services.proxy.controllers import get_page, get_static_resource, auth_token
# CONTROLLER HANDLER
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    if path in paths:
        response = get_page(environ)
    elif path.startswith('/static'):
        response = get_static_resource(environ)
    elif path == "/auth_user":
        response = auth_token(environ)
    elif path == '/register_user':
        print('trying to register')
        res = requests.post(ServiceUrl.AUTH + "/register_user", json=json_to_dict(read_body(environ)))
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
