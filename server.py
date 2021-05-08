import os

content_type = {'.html': 'text/html',
                '.css': 'text/css'
                }


# TEMPLATE RENDERING WITH CONTEXT
def render_template(template_name='index.html', context={}):
    template_name = f"templates/{template_name}"
    html_string = ""

    with open(template_name, 'r') as f:
        html_string = f.read()
        html_string = html_string.format(**context)

    return html_string


# RENDERING FILES SUCH AS IMAGES, CSS, ETC
def render_file(file_name):
    file_name = file_name[1:len(file_name)]
    file_string = ""

    with open(file_name, 'r') as f:
        file_string = f.read()

    return file_string


# CONTROLLERS
def home(environ):
    return render_template(template_name='index.html', context={"data": "ana are mere"})


def page_not_found(environ):
    return render_template(template_name='404.html')


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
