from authentication.instance.user_data import UserData
from authentication.jwt_util import jwt_encode
from request.renderer import render_template
from request.response_data import HttpStatus, ContentType
from server.database.models.user_model import User
from util.util import read_body, json_to_dict, dict_to_json


def home_renderer(environ) -> (str, str, []):
    data = render_template(template_name='index.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')})

    return data, HttpStatus.OK, [ContentType.HTML]


def login_renderer(environ) -> (str, str, []):
    return render_template(template_name='login.html', context={}), HttpStatus.OK, [ContentType.HTML]


def register_renderer(environ) -> (str, str, []):
    return render_template(template_name='register.html', context={}), HttpStatus.OK, [ContentType.HTML]


def topics_renderer(environ) -> (str, str, []):
    return render_template(template_name='topics_of_interest.html'), HttpStatus.OK, [ContentType.HTML]


def confirm_account_renderer(environ) -> (str, str, []):
    return render_template(template_name='confirm_account.html'), HttpStatus.OK, [ContentType.HTML]


def user_profile_renderer(environ):
    return render_template(template_name='user_profile.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')}), HttpStatus.OK, [ContentType.HTML]


def documentation_renderer(environ):
    return render_template(template_name='documentation.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')}), HttpStatus.OK, [ContentType.HTML]


def doc_renderer(environ):
    return render_template(template_name='doc.html')


def page_not_found_renderer(environ):
    return render_template(template_name='404.html')


# REST ENDPOINTS
def get_user_auth(environ) -> (str, str, []):

    body_dict = json_to_dict(read_body(environ))

    user = User(username=body_dict['username'], password=body_dict['password'])

    status = user.login()

    if not status['status']:
        return dict_to_json({'error': status['message']}), HttpStatus.NOT_FOUND, [ContentType.JSON]

    user = UserData(user.user_id, user.username, user.email)

    user_jwt_data = jwt_encode(user)

    data = {'userAuth': user_jwt_data}

    return dict_to_json(data), HttpStatus.OK, [ContentType.JSON]
