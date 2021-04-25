
def render_template(template_name='index.html', context={}):
    template_name = f"templates/{template_name}"
    html_string = ""

    with open(template_name, 'r') as f:
        html_string = f.read()
        html_string = html_string.format(**context)

    return html_string


def home(environ):
    return render_template(template_name='index.html', context={"data": "ana are mere"})


def page_not_found(environ):
    return render_template(template_name='404.html')


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    if path == "":
        data = home(environ)
    else:
        data = page_not_found(environ)

    data = data.encode("utf-8")

    start_response(
        f"200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ]
    )

    return iter([data])

# pipenv shell
# gunicorn server:app --reload

# the main documentation source: https://youtu.be/fe9t9DGPBuE
