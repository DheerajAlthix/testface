# import os

# ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")  # Default to development

# if ENVIRONMENT == "prod":
#     from .prod import *
# else:
#     from .dev import *


from split_settings.tools import include
from decouple import config

include('base.py')

if 'dev' == config('DJANGO_ENV', 'dev'):
    include('dev.py')
elif 'prod' == config('DJANGO_ENV', 'dev'):
    include('prod.py')