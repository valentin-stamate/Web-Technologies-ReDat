import os
import requests
from services.proxy.template_formatter import render_template
from util.instance.user import User
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
        response.payload = render_home(environ)
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
def render_home(environ):
    res = requests.get(ServiceUrl.SERVER + "/index.html")

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    return render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})


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


# REST ENDPOINTS
# def get_user_auth(environ) -> ResponseData:
#     response = ResponseData()
#
#     body_dict = json_to_dict(read_body(environ))
#
#     user = User(username=body_dict['username'], password=body_dict['password'])
#
#     status = user.login()
#
#     response.put(payload=dict_to_json({'error': status['message']}), status=HttpStatus.NOT_FOUND,
#                  headers=[ContentType.JSON])
#
#     if not status['status']:
#         return response
#
#     user = UserData(user.user_id, user.username, user.email)
#
#     user_jwt_data = jwt_encode(user)
#
#     data = {'userAuth': user_jwt_data}
#
#     response.put(payload=dict_to_json(data), status=HttpStatus.OK, headers = [ContentType.JSON])
#
#     return response

def get_auth_token(environ) -> ResponseData:
    response = ResponseData()

    body_dict = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.SERVER + "/get_auth_token", json=body_dict)

    response.payload = res.text
    response.status = "200"
    response.headers = [ContentType.JSON]

    return response
