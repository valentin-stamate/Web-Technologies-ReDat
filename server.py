import os
from request.content_type import *
from request.controllers import home, page_not_found
from request.renderer import render_file


# CONTROLLER HANDLER
def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    filename, file_extension = os.path.splitext(path)

    print(f"Requested file: {path}")

    if path == "":
        data = home(environ)
    elif path.startswith('/static'):
        data = render_file(path)
    else:
        data = page_not_found(environ)

    data = data.encode("utf-8")

    start_response(
        f"200 OK", [
            ("Content-Type", content_type.get(file_extension, 'text/html')),
            ("Content-Length", str(len(data)))
        ]
    )

    return iter([data])


# pipenv shell
# gunicorn server:app --reload

# the main documentation source: https://youtu.be/fe9t9DGPBuE
