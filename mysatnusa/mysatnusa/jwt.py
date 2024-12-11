import environ
import jwt

env = environ.Env()
environ.Env.read_env()

class JWTAuth:
    def __init__(self):
        self.secret = env('JWT_SECRET')

    def encode(self, payload):
        return jwt.encode(payload, self.secret, algorithm='HS256').decode("utf-8")

    def decode(self, token):
        return jwt.decode(token, self.secret, algorithms=['HS256'])