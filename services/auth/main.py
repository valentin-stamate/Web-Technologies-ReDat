import os


# CONTROLLER HANDLER
def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    data = ""

    headers = []
    response_status = "200 OK"

    if path == "":
        data = "Hello there. This is the auth service."
    elif path == "/auth_user":
        data = "dsad"

    data = data.encode("utf-8")

    response_headers = [("Content-Length", str(len(data)))]
    response_headers += headers

    start_response(
        response_status,
        response_headers
    )

    return iter([data])

