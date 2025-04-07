from enum import Enum
from rest_framework.response import Response


class HTTPStatus(Enum):
    success = (200, 'success')
    created = (201, 'created')
    accepted = (202, 'accepted')
    no_content = (204, 'no content')
    bad_request = (400, 'bad request')
    unauthorized = (401, 'unauthorized request')
    not_found = (404, 'resource not found')
    conflict = (409, 'duplicate conflict')
    unprocessable_entity = (422, 'unprocessable entity')
    method_failure = (420, 'method failure')
    error = (500, 'application error occurred')
    unauthorized_new = (402, 'unauthorized request')
    warning = (199, 'miscellaneous warning')
    large_response_data = (413, 'large response data')


class ResponseStatus:
    @classmethod
    def success(cls, data):
        return Response({"status": HTTPStatus.success.value[1], "payload": data}, status=HTTPStatus.success.value[0])

    @classmethod
    def created(cls, data):
        return Response({"status": HTTPStatus.created.value[1], "payload": data}, status=HTTPStatus.created.value[0])

    @classmethod
    def error(cls, error_message):
        return Response({"status": HTTPStatus.error.value[1], "error": error_message}, status=HTTPStatus.error.value[0])

    @classmethod
    def bad_request(cls, error_message):
        return Response({"status": HTTPStatus.bad_request.value[1], "error": error_message}, status=HTTPStatus.bad_request.value[0])

    @classmethod
    def unauthorized(cls, error_message):
        return Response({"status": HTTPStatus.unauthorized.value[1], "error": error_message}, status=HTTPStatus.unauthorized.value[0])

    @classmethod
    def not_found(cls, error_message):
        return Response({"status": HTTPStatus.not_found.value[1], "error": error_message}, status=HTTPStatus.not_found.value[0])

    @classmethod
    def not_data(cls, error_message):
        return Response({"status": HTTPStatus.no_content.value[1], "data_required": error_message}, status=HTTPStatus.no_content.value[0])



class UniversalMessage(Enum):
    system_error = "Something Unexpected happened. Please Contact to Administrator" 
    request_data_error = "Sending Incorrect Request payload format" 
    key_missing_error = "{} key Required field" 
    key_none_error = "{} key None" 
    incorrect_data_error = "{} data incorrect " 
    process_started = "Process Started. You will receive a notification when completed" 
    process_started_skip = "There are rows that were skipped due to an error, {}. You will receive a notification when process is completed."