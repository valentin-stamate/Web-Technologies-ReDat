from util.ResponseData import ResponseData
from util.request.response_data import ContentType


# CONTROLLER HANDLER
def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = "200"

    if path == "":
        response.payload = "The server service is working"

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response.headers
    )

    return iter([response.payload])

