from rest_framework.response import Response
from rest_framework import status

from .exceptions import _wrap_error_payload


def validation_error_response(serializer, *, status_code=status.HTTP_400_BAD_REQUEST):
    """Respuesta 400 con el mismo formato que el exception handler."""
    body = _wrap_error_payload(status_code, serializer.errors)
    return Response(body, status=status_code)
