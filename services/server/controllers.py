from services.server.database.models.topic_model import TopicModel
from services.server.database.models.user_model import UserModel
from services.server.database.models.user_topics_model import UserTopicModel
from services.server.renderer import render_file
from util.password_encryption import PasswordEncryption
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.util import read_body, json_to_dict, dict_to_json, timestamp_to_str


def make_user_admin(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))
    username = body['username']

    user = UserModel.get_by_username(username)['object']

    if user is None:
        response.status = HttpStatus.NOT_FOUND
        return response

    user.is_admin = True
    user.update()

    response.payload = dict_to_json({"message": "success"})

    return response


def remove_user_admin(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))
    username = body['username']

    user = UserModel.get_by_username(username)['object']

    if user is None:
        response.status = HttpStatus.NOT_FOUND
        return response

    user.is_admin = False
    user.update()

    return response


def admin_add_topic(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    topic_model = TopicModel(body['topic_name'])
    topic_model.save()

    response.payload = dict_to_json({'message': f"Topic {topic_model.name} saved."})

    return response


def admin_remove_topic(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    topic_model = TopicModel.get_by_name(body['topic_name'])['object']
    UserTopicModel.delete_topic_from_users(topic_model)
    topic_model.delete()

    response.payload = dict_to_json({'message': f"Topic {topic_model.name} deleted."})

    return response


def admin_get_user(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))
    username = body['username']

    user = UserModel.get_by_username(username)['object']

    if user is None:
        response.status = HttpStatus.NOT_FOUND
        response.payload = dict_to_json({"message": f"User {username} not found."})
        return response

    user.password = ''
    user.date_created = ''
    response.payload = dict_to_json(user.__dict__)

    return response


def admin_remove_user(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))
    username = body['username']

    user = UserModel.get_by_username(username)['object']

    if user is None:
        response.status = HttpStatus.NOT_FOUND
        return response

    UserTopicModel.delete_user_topics(user)
    user.delete()

    response.payload = dict_to_json({"message": f"User {user.username} deleted."})

    return response


def update_user(environ) -> ResponseData:
    response = ResponseData()
    response.status = HttpStatus.OK
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))
    response.headers = [ContentType.JSON]
    db_user = UserModel.get_by_id(body['id'])['object']

    if db_user.password != PasswordEncryption.encrypt_password(body['oldPassword'], db_user.date_created):
        response.payload = dict_to_json({'message': 'Wrong password'})
        response.status = HttpStatus.BAD_REQUEST
        return response

    if body['username'] != db_user.username:
        if not UserModel.get_by_username(body['username'])['object'] is None:
            response.payload = dict_to_json({'message': 'Username already taken'})
            response.status = HttpStatus.BAD_REQUEST
            return response

    db_user.username = body['username']
    db_user.lastname = body['lastname']
    db_user.firstname = body['firstname']
    db_user.email = body['email']

    if body['password'] != '':
        db_user.password = PasswordEncryption.encrypt_password(body['password'], db_user.date_created)

    if db_user.is_valid():
        db_user.update()
        response.payload = dict_to_json({'message': 'Success'})
        return response

    response.status = HttpStatus.BAD_REQUEST
    response.payload = dict_to_json({'message': 'Invalid fields'})
    return response


def delete_user_topic(environ):
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))

    user_model = UserModel.get_by_id(body['user_id'])['object']
    topic_model = TopicModel.get_by_id(body['topic_id'])['object']

    user_topic_model = UserTopicModel(user_model, topic_model)

    if not user_topic_model.delete():
        response.status = HttpStatus.BAD_REQUEST
        response.payload = dict_to_json({'message': 'Failure'})
        return response

    response.payload = dict_to_json({'message': 'Success'})
    return response


def add_user_topic(environ):
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))

    user_model = UserModel.get_by_id(body['user_id'])['object']
    topic_model = TopicModel.get_by_id(body['topic_id'])['object']

    user_topic_model = UserTopicModel(user_model, topic_model)

    if not user_topic_model.save():
        response.status = HttpStatus.BAD_REQUEST
        response.payload = dict_to_json({'message': 'Failure'})
        return response

    response.payload = dict_to_json({'message': 'Success'})

    return response


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

    status = new_user.is_valid()

    if not status['status']:
        response.payload = dict_to_json({'status': False, 'message': status['message']})
        response.status = HttpStatus.BAD_REQUEST
        return response

    status = new_user.save()

    res_json['message'] = status['message']

    response.payload = dict_to_json(res_json)
    if not status['status']:
        response.status = HttpStatus.BAD_REQUEST
        return response

    response.payload = dict_to_json(new_user.__dict__)
    return response
