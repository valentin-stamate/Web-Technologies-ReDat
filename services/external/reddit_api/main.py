from util.request.response_data import ContentType
from util.response_data import ResponseData


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    response.headers = [ContentType.JSON]
    if path == "":
        response.payload = "Hello there. This is the external api service."
    else:
        response.payload = "noy found"

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response_headers
    )

    return iter([response.payload])
