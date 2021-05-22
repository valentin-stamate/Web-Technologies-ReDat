from services.external.controllers import *
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from util.util import json_to_dict, read_body


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    response.headers = [ContentType.JSON]
    if path == "":
        response.payload = "Hello there. This is the external api service."
    elif path == '/statistic/general':
        response.status = HttpStatus.OK
        response.payload = (str(get_general_statistic()))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/upvote_ratio':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_upvote_ratio_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/comments':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_comments_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/ups_downs':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_ups_downs_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
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