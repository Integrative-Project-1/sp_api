"""
Manejo estándar de errores API (C5).

Formato:
  {
    "error": { "code": "...", "message": "...", "details": {...} },  // opcional details
    "detail": "..."   // compatibilidad con clientes que leen solo detail
  }
"""
from rest_framework.views import exception_handler

_STATUS_TO_CODE = {
    400: 'bad_request',
    401: 'unauthorized',
    403: 'forbidden',
    404: 'not_found',
    405: 'method_not_allowed',
    409: 'conflict',
    429: 'throttled',
    500: 'server_error',
}


def _wrap_error_payload(status_code, data):
    if isinstance(data, dict) and 'error' in data:
        return data

    if status_code == 400 and isinstance(data, dict) and 'detail' not in data:
        message = 'Los datos enviados no son válidos.'
        return {
            'error': {
                'code': 'validation_error',
                'message': message,
                'details': data,
            },
            'detail': message,
        }

    if isinstance(data, dict) and 'detail' in data:
        message = data['detail']
        if isinstance(message, list):
            message = message[0] if message else 'Error en la solicitud.'
    else:
        message = 'Error en la solicitud.'

    code = _STATUS_TO_CODE.get(status_code, 'error')
    payload = {
        'error': {
            'code': code,
            'message': str(message),
        },
        'detail': str(message),
    }
    if isinstance(data, dict) and 'detail' not in data:
        payload['error']['details'] = data
    return payload


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response
    response.data = _wrap_error_payload(response.status_code, response.data)
    return response
