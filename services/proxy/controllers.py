import os
import requests
from services.proxy.template_formatter import render_template
from util.request.content_type import content_type
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.service_url import ServiceUrl
from util.util import read_body, json_to_dict, dict_to_json


def get_page(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    path, file_extension = os.path.splitext(path)

    response = ResponseData()

    if path == "/" or path == "" or path == "/home":
        path = "/index"

    if path == "/index":
        response = render_home(environ)
    elif path == "/profile":
        response.payload = render_user_profile(environ)

    # Other pages that requires no other template or processing
    if path == "/register" or path == "/login" or path == "/doc" or path == "/documentation"\
            or path == "/confirm_account" or path == "/topics_of_interests":
        response.payload = requests.get(ServiceUrl.SERVER + path + ".html").text

    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


# RENDERING PAGES
def render_home(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]

    token = get_auth_token(environ)

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    res = requests.get(ServiceUrl.SERVER + "/index.html")

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    response.payload = render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})
    return response


def render_user_profile(environ):
    res = requests.get(ServiceUrl.SERVER + "/user_profile.html")

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    return render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})


# RETURN A RESOURCE FORM /static FOLDER
def get_static_resource(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    filename, file_extension = os.path.splitext(path)

    response = ResponseData()

    response.headers = [content_type.get(file_extension, 'text/html')]

    res = requests.get(ServiceUrl.SERVER + path)

    response.payload = res.text
    response.status = HttpStatus.OK

    return response


def auth_token(environ) -> ResponseData:
    response = ResponseData()

    body_dict = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.AUTH + "/auth_user", json=body_dict)

    response.payload = res.text
    response.status = str(res.status_code)
    response.headers = [ContentType.JSON]

    return response


def get_auth_token(environ) -> str or None:
    return get_cookies_as_dict(environ).get('user_auth', None)


def get_cookies_as_dict(environ) -> dict:
    cookies = environ['HTTP_COOKIE']
    cookies = cookies.split('; ')
    handler = {}

    for cookie in cookies:
        cookie = cookie.split('=')
        handler[cookie[0]] = cookie[1]
    return handler
