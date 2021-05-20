import datetime
import json
import time
from io import BytesIO


def current_timestamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def get_cookie(name, value, days=365) -> str:
    dt = datetime.datetime.now() + datetime.timedelta(days=days)
    fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    secs = days * 86400
    return '{}={}; Expires={}; Max-Age={}; Path=/'.format(name, value, fdt, secs)


def json_to_dict(value: str) -> []:
    return json.loads(value)


def dict_to_json(value: []) -> str:
    return json.dumps(value)


def read_body(environ) -> str:
    body: BytesIO = environ.get("wsgi.input")
    return body.read().decode('utf8').replace("'", '"')


def timestamp_to_str(timestamp) -> str:
    return timestamp.strftime("%m/%d/%Y, %H:%M:%S")
