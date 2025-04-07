import os


CORS_ALLOW_ALL_ORIGINS = True


# settings.py
APPEND_SLASH = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # Replace with Expo URL if using Expo
    "https://testface-6t3o.onrender.com",  # Replace with actual IP if testing on device
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
DEBUG = os.environ.get('DEBUG') == 'True'  # Converts it to actual boolean
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,https://testface-6t3o.onrender.com").split(",")


# settings.py
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False
