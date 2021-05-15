from services.auth.instance.user_data import UserData
from services.auth.jwt_util import jwt_encode
from util.ResponseData import ResponseData
from util.request.renderer import render_template
from util.request.response_data import HttpStatus, ContentType
from services.server.database.models.user_model import User
from util.util import read_body, json_to_dict, dict_to_json


def home_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='index.html',
                                       context={'top_bar': render_template('top_bar.html'),
                                                'footer': render_template('footer.html')})
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]

    return response


def login_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='login.html', context={})
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def register_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='register.html', context={})
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def topics_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='topics_of_interest.html')
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def confirm_account_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='confirm_account.html')
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def user_profile_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='user_profile.html',
                                       context={'top_bar': render_template('top_bar.html'),
                                                'footer': render_template('footer.html')})
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def documentation_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='documentation.html',
                                       context={'top_bar': render_template('top_bar.html'),
                                                'footer': render_template('footer.html')})
    response.headers = [ContentType.HTML]
    return response


def doc_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='doc.html')
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


def page_not_found_renderer(environ) -> ResponseData:
    response = ResponseData()

    response.payload = render_template(template_name='404.html')
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
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
