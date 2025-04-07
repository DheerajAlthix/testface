from .base import *

DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'riddhi',
        'USER': 'riddhi_user',
        'PASSWORD': 'joOCvRRvhJ0Q95Gmb8ctNLpZ3KaHG64m',
        'HOST': 'dpg-cvpoj2qdbo4c7393e76g-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",  # Stores the database in the project root
#     }
# }



STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'static'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'badgotidheeraj@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'huzg djya ewbl yopc')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
GOOGLE_SSO_PROJECT_ID = os.environ.get('GOOGLE_SSO_PROJECT_ID')
GOOGLE_SSO_CLIENT_SECRET = os.environ.get('GOOGLE_SSO_CLIENT_SECRET')

GOOGLE_SSO_ALLOWABLE_DOMAINS = ["gmail.com"]


# Cache configuration (using Django's default cache backend)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
