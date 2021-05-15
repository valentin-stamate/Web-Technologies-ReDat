
class ResponseData:

    def __init__(self):
        self.payload = ''
        self.status = ''
        self.headers = []

    def put(self, payload: str, status: str, headers: []):
        self.payload = payload
        self.headers = headers
        self.status = status

