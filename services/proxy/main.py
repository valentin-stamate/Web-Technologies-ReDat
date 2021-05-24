import requests

from services.proxy.controllers import get_page, get_static_resource, auth_user, register_user, user_delete_topic, \
    all_topics, user_topics, user_add_topic, up_vote_ratio, statistic_general, statistic_comments, statistic_ups_downs, \
    statistic_downs
from util.pages import paths
from util.request.response_data import HttpStatus, ContentType
from util.response_data import ResponseData
from util.service_url import ServiceUrl
from util.util import json_to_dict, read_body


# CONTROLLER HANDLER
def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    if path in paths:
        response = get_page(environ)
    elif path.startswith('/static'):
        response = get_static_resource(environ)
    elif path == "/auth_user":
        response = auth_user(environ)
    elif path == '/register_user':
        response = register_user(environ)
    elif path == '/update_user':
        body = json_to_dict(read_body(environ))
        res = requests.post(ServiceUrl.AUTH + "/check_user_auth",
                            headers={'Authorization': environ.get("HTTP_AUTHORIZATION")},
                            json=body)
        user_data = json_to_dict(res.text)
        body['id'] = user_data['user_id']
        if str(res.status_code) == HttpStatus.OK:
            res = requests.post(ServiceUrl.SERVER + "/update_user", json=body)
            response.payload = res.text
    elif path == '/user_delete_topic':
        response = user_delete_topic(environ)
    elif path == '/user_add_topic':
        response = user_add_topic(environ)
    elif path == "/user_topics":
        response = user_topics(environ)
    elif path == "/all_topics":
        response = all_topics(environ)
    elif path == "/statistic/upvote_ratio":
        response = up_vote_ratio(environ)
    elif path == "/statistic/general":
        response = statistic_general(environ)
    elif path == "/statistic_comments":
        response = statistic_comments(environ)
    elif path == "/statistic_ups_downs":
        response = statistic_ups_downs(environ)
    elif path == "/statistic/downs":
        response = statistic_downs(environ)
    else:
        response.status = HttpStatus.NOT_FOUND
        response.payload = "Page not found."
        response.headers = [ContentType.HTML]

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(
        response.status,
        response_headers
    )

    return iter([response.payload])
