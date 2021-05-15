import os
import requests
from services.auth.instance.user_data import UserData
from services.auth.jwt_util import jwt_encode
from util.request.content_type import content_type
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from services.server.database.models.user_model import User
from util.service_url import ServiceUrl
from util.util import read_body, json_to_dict, dict_to_json


def get_page(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    filename, file_extension = os.path.splitext(path)

    response = ResponseData()

    if filename == "/" or filename == "" or filename == "/home":
        filename = "/index"

    res = requests.get(ServiceUrl.SERVER + filename + ".html")

    response.payload = res.text
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def get_resource(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    filename, file_extension = os.path.splitext(path)

    response = ResponseData()

    response.headers.append(content_type.get(file_extension, 'text/html'))

    res = requests.get(ServiceUrl.SERVER + path)

    response.payload = res.text
    response.status = HttpStatus.OK

    return response


# REST ENDPOINTS
def get_user_auth(environ) -> ResponseData:
    response = ResponseData()

    body_dict = json_to_dict(read_body(environ))

    user = User(username=body_dict['username'], password=body_dict['password'])

    status = user.login()

    response.put(payload=dict_to_json({'error': status['message']}), status=HttpStatus.NOT_FOUND,
                 headers=[ContentType.JSON])

    if not status['status']:
        return response

    user = UserData(user.user_id, user.username, user.email)

    user_jwt_data = jwt_encode(user)

    data = {'userAuth': user_jwt_data}

    response.put(payload=dict_to_json(data), status=HttpStatus.OK, headers = [ContentType.JSON])

    return response
