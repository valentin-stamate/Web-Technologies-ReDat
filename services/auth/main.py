# CONTROLLER HANDLER
from services.server.database.models import user_model
from util.util import json_to_dict, read_body


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ""

    headers = []
    response_status = "200 OK"

    if path == "":
        response = "Hello there. This is the auth service."
    elif path == "/auth_user":
        response = "dsad"
    elif path == "/register_user":
        register_response = register(environ)
        response = register_response['message']

    response = response.encode("utf-8")

    response_headers = [("Content-Length", str(len(response)))]
    response_headers += headers

    start_response(
        response_status,
        response_headers
    )

    return iter([response])


# REGISTER NEW USER
def register(environ) -> dict:
    body_dict = json_to_dict(read_body(environ))

    db_user = user_model.UserModel.get_by_username(body_dict['username'])['object']

    if db_user is not None:
        return {'status': False, 'message': "Username already exists"}

    new_user = user_model.UserModel(body_dict['username'], body_dict['firstname'], body_dict['lastname'], body_dict['email'],
                                    body_dict['password'])
    if not new_user.is_valid()['status']:
        return {'status': False, 'message': new_user.is_valid()['message']}
    new_user.save()
    return {'status': True, 'message': "User created"}
