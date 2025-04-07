import uuid
import json
import requests
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer

from google.auth.transport import requests as google_requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings



# Custom imports

