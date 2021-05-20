from services.server.database.models.user_model import UserModel
from services.server.renderer import render_file
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.util import read_body, json_to_dict, dict_to_json, timestamp_to_str


def get_file(path):
    response = ResponseData()

    response.payload = render_file(path)
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


# def auth_user(environ):
#     response = ResponseData()
#     response.headers = [ContentType.JSON]
#
#     response_body = json_to_dict(read_body(environ))
#
#     user = UserModel(username=response_body['username'], password=response_body['password'])
#
#     status = user.login()
#
#     if not status['status']:
#         response.payload = status['message']
#         response.status = HttpStatus.BAD_REQUEST
#         return response
#
#     user_data = UserJWTData(user_id=user.user_id, username=user.username, email=user.email)
#     token = jwt_encode(user_data)
#
#     response.payload = dict_to_json({'token': token})
#     response.status = HttpStatus.OK
#
#     return response


def check_user(environ):
    response = ResponseData()
    response.headers = [ContentType.JSON]

    response_body = json_to_dict(read_body(environ))
    user = UserModel(username=response_body['username'], password=response_body['password'])

    status = user.login()

    response.payload = dict_to_json(status)

    if not status['status']:
        response.status = HttpStatus.BAD_REQUEST
        response.payload = status['message']
        return response

    user.password = ""

    user.date_created = str()
    response.payload = dict_to_json(user.__dict__)

    return response


def user_data(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    user_id = json_to_dict(read_body(environ))['id']
    user_info = UserModel.get_by_id(user_id)['object']

    user_info.password = ''
    user_info.date_created = timestamp_to_str(user_info.date_created)
    user_info = user_info.__dict__

    response.payload = dict_to_json(user_info)

    return response


def register_user(environ) -> ResponseData:
    response = ResponseData()

    body = json_to_dict(read_body(environ))
    new_user = UserModel(body['username'], body['firstname'], body['lastname'], body['email'], body['password'])

    res_json = {}

    status = new_user.save()

    res_json['message'] = status['message']

    response.payload = dict_to_json(res_json)
    if not status['status']:
        response.status = HttpStatus.BAD_REQUEST
        return response

    response.payload = dict_to_json(new_user.__dict__)
    return response
