from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler
from sentry_sdk import capture_exception

from apps.core.response_resource import ResponseResource


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    message_error = exc.detail if hasattr(exc, 'detail') else str(exc)
    if response is not None:
        status_code = response.status_code
        exc_class = exc.__class__.__name__
        if exc_class in ['AuthenticationFailed', 'NotAuthenticated']:
            status_code = status.HTTP_401_UNAUTHORIZED
        if exc_class == 'ValidationError':
            if isinstance(exc.detail, list) and isinstance(exc.detail[0], ErrorDetail):
                message_error = exc.detail[0]
            else:
                message_error = get_errors_messages(exc.detail)

        response.status_code = status_code
    else:
        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        message_error = None
        capture_exception(exc)

    response.data = ResponseResource(status=False, errors=message_error).data
    return response


def get_errors_messages(detail, prefix=""):
    errors = {}
    if isinstance(detail, list):
        for i, item in enumerate(detail):
            key = f"{prefix}[{i}]" if prefix else ''
            errors.update(get_errors_messages(item, prefix=key))
    elif isinstance(detail, dict):
        for key, value in detail.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            errors.update(get_errors_messages(value, prefix=new_prefix))
    else:
        if prefix[-1] == ']':
            prefix = prefix[:-3]
        errors[prefix] = detail

    return errors
