import os
import requests
from services.proxy.template_formatter import render_template
from util.request.content_type import content_type
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.service_url import ServiceUrl
from util.util import read_body, json_to_dict, dict_to_json

admin_link = '<div><a href="/admin_users"><b>Admin</b></a></div>'


def admin_get_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    username = body['username']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': username})

    response.status = str(res.status_code)
    response.payload = res.text

    return response


def admin_remove_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    username = body['username']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_remove_user", json={'username': username})

    response.payload = res.text

    return response


def admin_add_topic(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    topic = body['topic_name']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_add_topic", json={'topic_name': topic})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def admin_remove_topic(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    topic = body['topic_name']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_remove_topic", json={'topic_name': topic})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def make_user_admin(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    username = body['username']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_add_admin", json={'username': username})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def remove_user_admin(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']
    username = body['username']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) != HttpStatus.OK:
        response.status = str(res.status_code)
        response.payload = res.text
        return response

    user_data = json_to_dict(res.text)
    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = dict_to_json({"message": "Not allowed"})
        return response

    res = requests.post(ServiceUrl.SERVER + "/admin_remove_admin", json={'username': username})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


#


def last_posts(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/last_posts", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def check_comments(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/check_new", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def csv_upvote_ratio(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.PLAIN]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/api/statistic/csv/upvote_ratio", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def csv_comments(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.PLAIN]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/api/statistic/csv/comments", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def csv_ups(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.PLAIN]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/api/statistic/csv/ups", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def csv_downs(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.PLAIN]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/api/statistic/csv/downs", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def statistic_downs(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.SVG]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/statistic/downs", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def statistic_ups_downs(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.SVG]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/statistic/ups_downs", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def statistic_comments(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.SVG]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/statistic/comments", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def up_vote_ratio(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.SVG]

    body = json_to_dict(read_body(environ))

    res = requests.get(ServiceUrl.EXTERNAL + "/statistic/upvote_ratio", json=body)

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def statistic_general(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.SVG]

    res = requests.get(ServiceUrl.EXTERNAL + "/api/statistic/general")

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def all_topics(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]

    res = requests.get(ServiceUrl.SERVER + "/all_topics")

    response.status = str(res.status_code)
    response.payload = res.text
    return response


def user_topics(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': body['token']})
    user_data = json_to_dict(res.text)
    res = requests.get(ServiceUrl.SERVER + "/user_topics", json={'id': user_data['user_id']})

    response.payload = res.text

    return response


def user_add_topic(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    user_data = json_to_dict(res.text)

    user_id = user_data['user_id']
    topic_id = body['topic_id']

    res = requests.post(ServiceUrl.SERVER + "/add_user_topic", json={'user_id': user_id, 'topic_id': topic_id})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def user_delete_topic(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]
    response.status = HttpStatus.OK

    body = json_to_dict(read_body(environ))
    token = body['token']

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    user_data = json_to_dict(res.text)

    user_id = user_data['user_id']
    topic_id = body['topic_id']

    res = requests.post(ServiceUrl.SERVER + "/delete_user_topic", json={'user_id': user_id, 'topic_id': topic_id})

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def get_page(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    path, file_extension = os.path.splitext(path)

    response = ResponseData()

    if path == "/" or path == "" or path == "/home":
        path = "/index"

    if path == "/index":
        response = render_home(environ)
    elif path == "/admin_users":
        response = admin_render_users(environ)
    elif path == "/admin_topics":
        response = admin_render_topics(environ)
    elif path == "/profile":
        response = render_user_profile(environ)
    elif path == "/topics":
        response = render_topics(environ)
    # Other pages that requires no other template or processing
    if path == "/register" or path == "/login" or path == "/doc" \
            or path == "/confirm_account" or path == "/api_documentation" \
            or path == "/how_to_use":
        response.payload = requests.get(ServiceUrl.SERVER + path + ".html").text

    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


# RENDERING PAGES
def render_topics(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]
    response.status = HttpStatus.OK

    token = get_auth_token(environ)

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    user_data = json_to_dict(res.text)

    topics_page = requests.get(ServiceUrl.SERVER + "/topics.html").text

    response.payload = render_template(topics_page, {'username': user_data['username']})

    return response


def admin_render_users(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]

    token = get_auth_token(environ)

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    user_data = json_to_dict(res.text)

    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = 'Unauthorized'
        response.headers = [ContentType.HTML]
        return response

    res = requests.get(ServiceUrl.SERVER + "/admin_users.html")

    user_res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(user_res.text)

    admin = ''
    if user_data['is_admin']:
        admin = admin_link

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username'], 'admin_link': admin})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    response.payload = render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})
    return response


def admin_render_topics(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]

    token = get_auth_token(environ)

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    user_data = json_to_dict(res.text)

    res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(res.text)

    if not user_data['is_admin']:
        response.status = HttpStatus.UNAUTHORIZED
        response.payload = 'Unauthorized'
        response.headers = [ContentType.HTML]
        return response

    res = requests.get(ServiceUrl.SERVER + "/admin_topics.html")

    user_res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(user_res.text)

    admin = ''
    if user_data['is_admin']:
        admin = admin_link

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username'], 'admin_link': admin})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    response.payload = render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})
    return response


def render_home(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]

    token = get_auth_token(environ)

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    user_data = json_to_dict(res.text)

    res = requests.get(ServiceUrl.SERVER + "/index.html")

    user_res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(user_res.text)

    admin = ''
    if user_data['is_admin']:
        admin = admin_link

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username'], 'admin_link': admin})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    response.payload = render_template(res.text, {'top_bar': top_bar_html, 'footer': footer_html})
    return response


def register_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    res = requests.post(ServiceUrl.AUTH + "/register_user", json=json_to_dict(read_body(environ)))

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def render_user_profile(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.HTML]
    response.status = HttpStatus.OK

    token = get_auth_token(environ)

    if token is None:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    res = requests.post(ServiceUrl.AUTH + "/check_user_auth", headers={'Authorization': token})

    if str(res.status_code) == HttpStatus.UNAUTHORIZED:
        res = requests.post(ServiceUrl.SERVER + "/redirect.html")

        response.payload = res.text
        response.status = str(res.status_code)
        return response

    user_data = json_to_dict(res.text)

    user_res = requests.post(ServiceUrl.SERVER + "/admin_get_user", json={'username': user_data['username']})
    user_data = json_to_dict(user_res.text)

    admin = ''
    if user_data['is_admin']:
        admin = admin_link

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username'], 'admin_link': admin})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    res = requests.get(ServiceUrl.SERVER + "/user_profile.html")

    user_data = requests.get(ServiceUrl.SERVER + "/user_data", json={'id': user_data['user_id']}).text
    user_data = json_to_dict(user_data)

    context = {'top_bar': top_bar_html, 'footer': footer_html}
    context.update(user_data)

    response.payload = render_template(res.text, context)
    return response


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


def auth_user(environ) -> ResponseData:
    response = ResponseData()
    response.headers = [ContentType.JSON]

    body_dict = json_to_dict(read_body(environ))

    res = requests.post(ServiceUrl.AUTH + "/auth_user", json=body_dict)

    response.payload = res.text
    response.status = str(res.status_code)

    return response


def get_auth_token(environ) -> str or None:
    cookies = get_cookies_as_dict(environ)

    if cookies is None:
        return None

    return cookies.get('user_auth', None)


def get_cookies_as_dict(environ) -> dict or None:
    try:
        cookies = environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        handler = {}

        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]
        return handler
    except:
        return None
