class HttpStatus:
    OK = "200"
    NOT_FOUND = "404"
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    REDIRECT = "301"


class ContentType:
    HTML = ("Content-Type", "text/html")
    CSS = ("Content-Type", "text/css")
    SVG = ("Content-Type", "image/svg+xml")
    PNG = ("Content-Type", "image/png")
    JPG = ("Content-Type", "image/jpeg")
    JS = ("Content-Type", "text/javascript")
    JSON = ("Content-Type", "text/json")
    PLAIN = ("Content-Type", "text/plain")
    CSV = ("Content-Type", "text/csv")
