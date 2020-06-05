from app.settings.base import *
from datetime import timedelta

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

URL_VIEW_MENU = 'http://localhost:4200/menu/'

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
)

SECRET_KEY = '50uo*w-*dqwnv5*_+@x+mn(yrf_94+eaasdasfa3$foz%i0!n9i!m1f+d'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'meal_manager.utils.jwt_token.jwt_encode_handler',
    'JWT_DECODE_HANDLER':
    'meal_manager.utils.jwt_token.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER':
    'meal_manager.utils.jwt_token.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_token.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'meal_manager.utils.jwt_token.jwt_response_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
    'meal_manager.utils.jwt_token.jwt_get_email_from_payload_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(hours = 168),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(hours = 24),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'meal_db',
        'USER': 'mealuser',
        'PASSWORD': 'mealpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#slack credentials
CLIENT_ID = '1183681473328.1160708526483'
CLIENT_SECRET = 'a9c0737feaf51d502e6f59107c3802a2'
VERIFICATION_TOKEN = 'Wdnuu0jFG1IYABtYpNFstYcR'
BOT_USER_ACCESS_TOKEN = 'xoxb-1183681473328-1166686218532-3SFXtMGfQe0uHJK7go3wjCzp'


# Celery application definition
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
DJANGO_CELERY_BEAT_TZ_AWARE = False