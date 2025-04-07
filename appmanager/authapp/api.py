from rest_framework import versioning
from rest_framework.versioning import URLPathVersioning
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class APIVersioning(URLPathVersioning):
    default_version = 'v1'
    allowed_versions = ['v1', 'v2']
    version_param = 'version'

def api_response(success=True, message="", data=None, status_code=200):
    """
    Standard API response format
    """
    response = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return response

def error_response(message, status_code=400):
    """
    Standard error response format
    """
    return api_response(
        success=False,
        message=message,
        status_code=status_code
    )

def success_response(data=None, message="Success"):
    """
    Standard success response format
    """
    return api_response(
        success=True,
        message=message,
        data=data
    )

# Common swagger parameters
common_parameters = {
    'Authorization': openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer token for authentication",
        type=openapi.TYPE_STRING
    ),
    'Content-Type': openapi.Parameter(
        'Content-Type',
        openapi.IN_HEADER,
        description="Content type of the request",
        type=openapi.TYPE_STRING,
        default='application/json'
    ),
}

# Common response schemas
common_responses = {
    '400': openapi.Response(
        description="Bad Request",
        examples={
            "application/json": {
                "success": False,
                "message": "Invalid input data"
            }
        }
    ),
    '401': openapi.Response(
        description="Unauthorized",
        examples={
            "application/json": {
                "success": False,
                "message": "Authentication credentials were not provided"
            }
        }
    ),
    '403': openapi.Response(
        description="Forbidden",
        examples={
            "application/json": {
                "success": False,
                "message": "You do not have permission to perform this action"
            }
        }
    ),
    '404': openapi.Response(
        description="Not Found",
        examples={
            "application/json": {
                "success": False,
                "message": "Resource not found"
            }
        }
    ),
    '500': openapi.Response(
        description="Internal Server Error",
        examples={
            "application/json": {
                "success": False,
                "message": "An unexpected error occurred"
            }
        }
    ),
} 