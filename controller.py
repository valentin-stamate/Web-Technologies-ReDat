import datetime
import os
from request.content_type import *
from request.controllers import home_renderer, page_not_found_renderer, login_renderer, register_renderer, \
    topics_renderer, confirm_account_renderer, user_profile_renderer, documentation_renderer, doc_renderer, \
    get_user_auth
from request.renderer import render_file


# CONTROLLER HANDLER
from util.util import get_cookie


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    filename, file_extension = os.path.splitext(path)

    headers = []
    response_status = "200 OK"

    if path == "" or path == "/home":
        data, response_status, headers = home_renderer(environ)
    elif path == "/login":
        data, response_status, headers = login_renderer(environ)
    elif path == "/register":
        data, response_status, headers = register_renderer(environ)
    elif path == "/topics":
        data, response_status, headers = topics_renderer(environ)
    elif path == "/confirm_account":
        data, response_status, headers = confirm_account_renderer(environ)
    elif path == "/profile":
        data, response_status, headers = user_profile_renderer(environ)
    elif path == "/documentation":
        data, response_status, headers = documentation_renderer(environ)
    elif path == "/doc":
        data = doc_renderer(environ)
    elif path.startswith('/static'):
        headers.append(content_type.get(file_extension, 'text/html'))
        data = render_file(path)
    # REST ENDPOINTS TODO split this into a microservice
    elif path == "/get_user_auth":
        data, response_status, headers = get_user_auth(environ)
    else:
        data = page_not_found_renderer(environ)

    data = data.encode("utf-8")

    response_headers = [("Content-Length", str(len(data)))]
    response_headers += headers

    start_response(
        response_status,
        response_headers
    )

    return iter([data])


# pipenv shell
# gunicorn server:app --reload
