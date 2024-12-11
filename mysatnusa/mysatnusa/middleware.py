import jwt
from functools import wraps
from mysatnusa.jwt import JWTAuth
from mysatnusa.response import Response
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from . import settings
from common.transaction_helper import jwt_uuid_conveter
import traceback
import datetime
from common.transaction_helper import *

# Function to decode JWT token
def decode(token):
    if token is None:
        raise Exception("No token provided")

    token_parts = str(token).split(' ')
    if len(token_parts) != 2 or token_parts[0] != 'Bearer':
        raise Exception("Invalid token format")

    try:
        # Decode the token with the secret key
        payload = jwt.decode(token_parts[1], settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

# JWT-required decorator
def jwtRequired(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            # Extract the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response.badRequest(request, message="Authorization header is missing", messagetype="E")

            # Decode the token and extract payload
            payload = decode(auth_header)

            # Attach payload details to the request
            request.jwt_payload = payload
            request.jwt_uuid = payload.get('uuid')
            request.jwt_user_id = jwt_uuid_conveter(request.jwt_uuid)  # Custom conversion function
            request.jwt_badge_no = payload.get('badge_no')
            request.jwt_fullname = payload.get('fullname')

        except Exception as e:
            # Return error if something goes wrong
            return Response.badRequest(request, message=str(e), messagetype="E")

        # Proceed with the original view function
        return fn(request, *args, **kwargs)

    return wrapper

# Custom middleware to return a JSON response
class JsonErrorMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Handle 404 error
        if response.status_code == 404:
            response_data = {
                'status_code': 404,
                'message': "Page not found",
                'messagetype': "E",
                'data': [],
            }
            return JsonResponse(response_data, status=404)

        # Handle 401 error
        elif response.status_code == 401:
            response_data = {
                'status_code': 401,
                'message': "Unauthorized access",
                'messagetype': "E",
                'data': [],
            }
            return JsonResponse(response_data, status=401)

        # Handle 403 error
        elif response.status_code == 403:
            response_data = {
                'status_code': 403,
                'message': "Forbidden access",
                'messagetype': "E",
                'data': [],
            }
            return JsonResponse(response_data, status=403)

        # Handle 500 error
        elif response.status_code == 500:
            response_data = {
                'status_code': 500,
                'message': "Internal server error",
                'messagetype': "E",
                'data': [],
            }
            return JsonResponse(response_data, status=500)

        return response