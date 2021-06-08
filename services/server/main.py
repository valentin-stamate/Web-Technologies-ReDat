import os

from services.server.controllers import get_file, admin_get_user, admin_remove_user
from services.server.controllers import user_data, register_user, check_user, user_topics, all_topics, \
    delete_user_topic, add_user_topic, update_user
from util.pages import pages
from util.request.content_type import content_type
from util.request.response_data import ContentType
from util.response_data import ResponseData


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    filename, file_extension = os.path.splitext(path)
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()
    response.status = "200"

    if path == "":
        response.payload = "The server service is working"

    # Page Requests
    if path.startswith('/static'):
        response = get_file(path)
        response.headers.append(content_type.get(file_extension, ContentType.HTML))
    elif path in pages:
        response = get_file("/templates" + path)
        response.headers = [ContentType.HTML]
    elif path == "/check_user":
        response = check_user(environ)
    elif path == '/register_user':
        response = register_user(environ)
    elif path == '/update_user':
        response = update_user(environ)
    elif path == '/user_data':
        response = user_data(environ)
    elif path == '/user_topics':
        response = user_topics(environ)
    elif path == '/all_topics':
        response = all_topics(environ)
    elif path == "/delete_user_topic":
        response = delete_user_topic(environ)
    elif path == "/add_user_topic":
        response = add_user_topic(environ)
    elif path == "/admin_get_user":
        response = admin_get_user(environ)
    elif path == "/admin_remove_user":
        response = admin_remove_user(environ)
    elif path == "/admin_add_topic":
        response = admin_add_topic(environ)
    elif path == "/admin_remove_topic":
        response = admin_remove_topic(environ)
    else:
        response.payload = "Not found"
        response.headers = [ContentType.HTML]
        response.status = "404"
    # User Requests

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(

        response.status,
        response_headers
    )
    return iter([response.payload])
