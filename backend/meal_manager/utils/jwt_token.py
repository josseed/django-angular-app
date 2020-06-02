from django.conf import settings
from datetime import *
from calendar import timegm
from rest_framework_jwt.settings import api_settings
import jwt

def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'email': user.email,
        'first_name': user.first_name,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }

def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.
    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'token': token,   
    }

def jwt_encode_handler(payload, context=None):
    return jwt.encode(
        payload,
        settings.JWT_AUTH['JWT_SECRET_KEY'],
        settings.JWT_AUTH['JWT_ALGORITHM'],
    ).decode('utf-8')


def jwt_decode_handler(token, context=None):
    return jwt.decode(
        token,
        settings.JWT_AUTH['JWT_SECRET_KEY'],
        settings.JWT_AUTH['JWT_VERIFY'],
        options = {
             'verify_exp': settings.JWT_AUTH['JWT_VERIFY_EXPIRATION'],
        },
        leeway = settings.JWT_AUTH['JWT_LEEWAY'],
        audience = settings.JWT_AUTH['JWT_AUDIENCE'],
        issuer = settings.JWT_AUTH['JWT_ISSUER'],
        algorithms = [settings.JWT_AUTH['JWT_ALGORITHM']],
    )

def jwt_get_email_from_payload_handler(payload):
    return payload.get('email')