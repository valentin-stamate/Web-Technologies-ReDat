from services.server.renderer import render_file
from util.response_data import ResponseData
from util.request.response_data import HttpStatus, ContentType


def get_file(path):
    response = ResponseData()

    response.payload = render_file(path)
    response.status = HttpStatus.OK
    response.headers = [ContentType.HTML]
    return response
