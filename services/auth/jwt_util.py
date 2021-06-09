import jwt
from jwt import InvalidSignatureError

from util.instance.user_jwt_data import UserJWTData
from secrets import JWT_SECRET_KEY, JWT_ALGORITHM


def jwt_encode(payload: UserJWTData) -> str:
    return jwt.encode(payload.__dict__, JWT_SECRET_KEY, JWT_ALGORITHM)


def jwt_decode(jwt_encoded: str) -> UserJWTData or None:
    try:
        dict_res = jwt.decode(jwt_encoded, JWT_SECRET_KEY, [JWT_ALGORITHM])
        return UserJWTData(dict_res['user_id'], dict_res['username'], dict_res['email'])
    except Exception as e:
        return None


def jwt_check(jwt_encoded: str) -> bool:
    try:
        user_payload = jwt_decode(jwt_encoded)

        if user_payload is None:
            return False

        return jwt_encoded == jwt_encode(user_payload)
    except InvalidSignatureError as e:
        return False
