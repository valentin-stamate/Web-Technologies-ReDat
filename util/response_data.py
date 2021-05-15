from util.request.response_data import ContentType


class ResponseData:

    def __init__(self):
        self.payload = ''
        self.status = '200'
        self.headers = [ContentType.HTML]

    def put(self, payload: str, status: str, headers: []):
        self.payload = payload
        self.headers = headers
        self.status = status

