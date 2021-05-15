import os
from services.server.controllers import get_file, login_user
from util.pages import paths, pages
from util.request.content_type import content_type
from util.response_data import ResponseData
from util.request.response_data import ContentType


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
    elif path == "/get_auth_token":
        response = login_user(environ)
    else:
        response.payload = "Not found"
        response.headers = [ContentType.HTML]
        response.status = "404"

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response_headers
    )

    return iter([response.payload])

