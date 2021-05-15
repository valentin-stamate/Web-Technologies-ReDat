import os

from util.ResponseData import ResponseData
from util.request.content_type import *
from services.proxy.controllers import home_renderer, page_not_found_renderer, login_renderer, register_renderer, \
    topics_renderer, confirm_account_renderer, user_profile_renderer, documentation_renderer, doc_renderer, \
    get_user_auth
from services.server.renderer import render_file


# CONTROLLER HANDLER


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    filename, file_extension = os.path.splitext(path)

    response = ResponseData()

    if path == "" or path == "/home":
        response = home_renderer(environ)
    elif path == "/login":
        response = login_renderer(environ)
    elif path == "/register":
        response = register_renderer(environ)
    elif path == "/topics":
        response = topics_renderer(environ)
    elif path == "/confirm_account":
        response = confirm_account_renderer(environ)
    elif path == "/profile":
        response = user_profile_renderer(environ)
    elif path == "/documentation":
        response = documentation_renderer(environ)
    elif path == "/doc":
        response = doc_renderer(environ)
    elif path.startswith('/static'):
        response.headers.append(content_type.get(file_extension, 'text/html'))
        response.payload = render_file(path)
        response.status = "200"
    elif path == "/auth_user":
        data, response_status, headers = get_user_auth(environ)
    else:
        data = page_not_found_renderer(environ)

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response.headers
    )

    return iter([response.payload])

