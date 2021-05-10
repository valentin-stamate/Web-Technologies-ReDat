import os
from request.content_type import *
from request.controllers import home_renderer, page_not_found_renderer, login_renderer, register_renderer, \
    topics_renderer, confirm_account_renderer, user_profile_renderer, documentation_renderer, doc_renderer
from request.renderer import render_file


# CONTROLLER HANDLER
def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    filename, file_extension = os.path.splitext(path)

    print(f"Requested file: {path}")

    if path == "" or path == "/home":
        data = home_renderer(environ)
    elif path == "/login":
        data = login_renderer(environ)
    elif path == "/register":
        data = register_renderer(environ)
    elif path == "/topics":
        data = topics_renderer(environ)
    elif path == "/confirm_account":
        data = confirm_account_renderer(environ)
    elif path == "/profile":
        data = user_profile_renderer(environ)
    elif path == "/documentation":
        data = documentation_renderer(environ)
    elif path == "/doc":
        data = doc_renderer(environ)
    elif path.startswith('/static'):
        data = render_file(path)
    else:
        data = page_not_found_renderer(environ)

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
