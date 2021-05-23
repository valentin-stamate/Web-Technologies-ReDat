from services.external.controllers import *
from services.external.reddit_api.reddit_data import get_hot_posts
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
from util.util import json_to_dict, read_body, dict_to_json


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()

    response.headers = [ContentType.JSON]
    if path == "":
        response.payload = "Hello there. This is the external api service."
    elif path == '/check_new':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        actual_com_nr = get_com_nr(body['topic'])
        notification = 0
        if actual_com_nr != int(body['comments_number']):
            notification = 1
        response.payload = dict_to_json({'notifications': notification, 'comments_number': actual_com_nr})
        response.headers = [ContentType.JSON]
    elif path == '/statistic/general':
        response.status = HttpStatus.OK
        response.payload = (str(get_general_statistic()))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/upvote_ratio':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_upvote_ratio_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/comments':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_comments_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
    elif path == '/statistic/ups_downs':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        response.payload = clean_svg(str(get_ups_downs_statistic(body['topic'])))
        response.headers = [ContentType.SVG]
    elif path == '/last_posts':
        body = json_to_dict(read_body(environ))
        response.status = HttpStatus.OK
        posts = get_hot_posts(body['topic'], limit=10)
        for post in posts:
            response.payload += post['data']['title'] + '\n'
        response.headers = [ContentType.PLAIN]
    elif path == '/statistic/csv/comments':
        response.status = HttpStatus.OK
        response.payload = get_csv_data('static/stats/csv/comments.csv')
        response.headers = [ContentType.PLAIN]
    elif path == '/statistic/csv/ups':
        response.status = HttpStatus.OK
        response.payload = get_csv_data('static/stats/csv/ups.csv')
        response.headers = [ContentType.PLAIN]
    elif path == '/statistic/csv/downs':
        response.status = HttpStatus.OK
        response.payload = get_csv_data('static/stats/csv/downs.csv')
        response.headers = [ContentType.PLAIN]
    elif path == '/statistic/csv/upvote_ratio':
        response.status = HttpStatus.OK
        response.payload = get_csv_data('static/stats/csv/upvote_ratio.csv')
        response.headers = [ContentType.PLAIN]
    elif path == '/statistic/topics':
        response.status = HttpStatus.OK
        response.payload = get_topics()
        response.headers = [ContentType.PLAIN]
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
