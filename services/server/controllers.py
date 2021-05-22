from services.server.database.models.topic_model import TopicModel
from services.server.database.models.user_model import UserModel
from services.server.database.models.user_topics_model import UserTopicModel
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


def user_topics(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    user_id = json_to_dict(read_body(environ))['id']
    user_model = UserModel.get_by_id(user_id)['object']

    topics = UserTopicModel.get_all(user_model)

    payload = '['

    for topic in topics:
        topic_json = dict_to_json(topic.__dict__)
        payload += topic_json + ','
    payload += ']'
    payload = payload.replace(",]", "]")

    response.payload = payload

    return response


def all_topics(environ):
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    topics = TopicModel.get_all()

    payload = '['

    for topic in topics:
        topic_json = dict_to_json(topic.__dict__)
        payload += topic_json + ','
    payload += ']'
    payload = payload.replace(",]", ']')

    response.payload = payload

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
