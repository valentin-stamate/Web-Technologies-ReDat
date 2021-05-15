import os
from services.server.controllers import get_file, login_user
from services.server.database.models.user_model import UserModel
from util.pages import paths, pages

from services.server.controllers import get_file
from services.server.database.models import user_model
from util.pages import pages
from util.request.content_type import content_type
from util.request.response_data import ContentType
from util.response_data import ResponseData
# CONTROLLER HANDLER
from util.util import read_body, json_to_dict


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
    elif path == "/get_auth_token":
        response = login_user(environ)
    else:
        response.payload = "Not found"
        response.headers = [ContentType.HTML]
        response.status = "404"
    # User Requests
    if path == '/register_user':
        body_dict = json_to_dict(read_body(environ))
        new_user = UserModel(body_dict['username'], body_dict['firstname'], body_dict['lastname'],
                             body_dict['email'],
                             body_dict['password'])
        new_user.save()

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(

        response.status,
        response_headers
    )
    return iter([response.payload])
