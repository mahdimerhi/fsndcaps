import json
import os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
SECRET_KEY = os.environ.get('SECRET_KEY')
CLIENT_ID = os.environ.get('CLIENT_ID')
CALLBACK_URL = os.environ.get('CALLBACK_URL')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'no header present'
        }, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or not header_parts:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'header is malformed'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'header must start with bearer'
        }, 401)

    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Permission not found.',
            'description': 'Permissions not included in JWT.'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


# Auth Header


def verify_decode_jwt(token):
    try:
        # GET THE PUBLIC KEY FROM AUTH0
        jsonurl = urlopen(f'{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        print(jwks)
        # GET THE DATA IN THE HEADER
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        print(e)

    # CHOOSE OUR KEY
    rsa_key = {'key'}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
