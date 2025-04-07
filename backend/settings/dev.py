DEBUG = False
import os

ALLOWED_HOSTS = [f'{os.environ.get('ALLOWED_HOSTS')}']

CORS_ALLOW_ALL_ORIGINS = True


# settings.py
APPEND_SLASH = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # Replace with Expo URL if using Expo
    "http://127.0.0.1:8000",  # Replace with actual IP if testing on device
]

CORS_ALLOWED_ORIGINS = ['http://localhost:8001']


CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)


# settings.py
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False
