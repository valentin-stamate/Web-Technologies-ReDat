import unittest
from unittest import TestCase
from authentication.instance.user_data import UserData
from authentication.jwt_util import jwt_encode, jwt_decode, jwt_check


class JwtTest(TestCase):

    def test_jwt(self):
        user_data = UserData(1, 'Valentin', 'stamatevalentin@gmail.com')

        encoded = jwt_encode(user_data)

        print(encoded)
        print(jwt_decode(encoded).user_id)

        user_data = UserData(2, 'Valentin', 'stamatevalentin@gmail.com')
        print(jwt_encode(user_data))

        print(jwt_check('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IlZhbGVudGluIiwiZW1haWwiOiJzdGFtYXRldmFsZW50aW5AZ21haWwuY29tIn0.bdYsE71Rt9y0ER8onXlCbqMdNorIoaZCdGObJ4IgnTk'))
        print(jwt_check('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IlZhbGVudGluIiwiZW1haWwiOiJzdGFtYXRldmFsZW50aW5AZ21haWwuY29tIn0.bdYsE71Rt9y0ER8onXlCbqMdNorIoaZCdGObJ4IgnTk'))


if __name__ == '__main__':
    unittest.main()
