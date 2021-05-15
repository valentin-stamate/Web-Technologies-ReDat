import re


def valid_username(username) -> bool:
    return len(username) > 7


def valid_name(name) -> bool:
    return len(name) > 2


def valid_email(email) -> bool:
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if not re.search(email_regex, email):
        return False
    return True


def valid_password(password) -> bool:
    return len(password) > 7
