import jwt
from jwt import InvalidSignatureError

from services.authentication.instance.user_data import UserData
from services.authentication.secrets import *


def jwt_encode(payload: UserData) -> str:
    return jwt.encode(payload.__dict__, JWT_SECRET_KEY, JWT_ALGORITHM)


def jwt_decode(jwt_encoded: str) -> UserData:
    dict_res = jwt.decode(jwt_encoded, JWT_SECRET_KEY, [JWT_ALGORITHM])
    return UserData(dict_res['user_id'], dict_res['username'], dict_res['email'])


def jwt_check(jwt_encoded: str) -> bool:
    try:
        user_payload = jwt_decode(jwt_encoded)
        return jwt_encoded == jwt_encode(user_payload)
    except InvalidSignatureError as e:
        return False
