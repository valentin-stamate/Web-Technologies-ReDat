import os

from services.server.controllers import user_data, register_user, check_user, user_topics, all_topics, \
    delete_user_topic, add_user_topic, update_user
from services.server.controllers import get_file
from services.server.database.models.user_model import UserModel
from util.pages import pages
from util.password_encryption import PasswordEncryption
from util.request.content_type import content_type
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from util.util import read_body, json_to_dict


# CONTROLLER HANDLER
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
