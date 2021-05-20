import os
import requests
from services.proxy.template_formatter import render_template
from util.request.content_type import content_type
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType
from util.service_url import ServiceUrl
from util.util import read_body, json_to_dict, dict_to_json


def get_page(environ) -> ResponseData:
    path = environ.get("PATH_INFO")
    path, file_extension = os.path.splitext(path)

    response = ResponseData()

    if path == "/" or path == "" or path == "/home":
        path = "/index"

    if path == "/index":
        response = render_home(environ)
    elif path == "/profile":
        response = render_user_profile(environ)
    elif path == "/documentation":
        response = render_documentation(environ)

    # Other pages that requires no other template or processing
    if path == "/register" or path == "/login" or path == "/doc"\
            or path == "/confirm_account" or path == "/topics_of_interests":
        response.payload = requests.get(ServiceUrl.SERVER + path + ".html").text

    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response


# RENDERING PAGES
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

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username']})

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

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username']})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    res = requests.get(ServiceUrl.SERVER + "/user_profile.html")

    user_data = requests.get(ServiceUrl.SERVER + "/user_data", json={'id': user_data['user_id']}).text
    user_data = json_to_dict(user_data)

    # TODO
    user_data['topics'] = {'Anime': 1, 'Funny': 2, 'Genshin Inpact': 3, 'It': 4, 'Movies': 5, 'Memes': 6}

    topic_item_template = "<div data-id={id}><button>x</button><b>{topic_name}</b></div>"

    topics_text = ''

    topic_item_list_template = '<div class="topic-list-item" data-id="{topic_id}">' \
                               '    <div><b>{topic_name}</b></div>' \
                               '    <div class="flex-right"></div>' \
                               '    <button class="button primary">Add</button>' \
                               '</div>'

    all_topics = {'Anime': 1, 'It': 2, 'Memes': 3, 'Casual': 4}

    all_topics_html = ''

    for topic in all_topics:
        all_topics_html += render_template(topic_item_list_template, {'topic_id': all_topics[topic], 'topic_name': topic})

    for topic in user_data['topics']:
        topics_text += render_template(topic_item_template, {'id': user_data['topics'][topic], 'topic_name': topic})

    context = {'top_bar': top_bar_html, 'footer': footer_html, 'rendered_topics': topics_text, 'all_topics': all_topics_html}
    context.update(user_data)

    response.payload = render_template(res.text, context)
    return response


def render_documentation(environ) -> ResponseData:
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

    top_bar_html = requests.get(ServiceUrl.SERVER + "/top_bar.html").text
    top_bar_html = render_template(top_bar_html, {'username': user_data['username']})

    footer_html = requests.get(ServiceUrl.SERVER + "/footer.html").text

    res = requests.get(ServiceUrl.SERVER + "/documentation.html")

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
