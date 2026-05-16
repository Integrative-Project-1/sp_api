"""Esquemas OpenAPI para actividades y subtareas (C5)."""
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    inline_serializer,
)
from rest_framework import serializers

from .serializers import ActivityDetailSerializer, ActivityListSerializer, SubtaskSerializer

ERROR_RESPONSE = OpenApiResponse(
    response=inline_serializer(
        name='ApiError',
        fields={
            'error': inline_serializer(
                name='ApiErrorBody',
                fields={
                    'code': serializers.CharField(),
                    'message': serializers.CharField(),
                    'details': serializers.DictField(required=False),
                },
            ),
            'detail': serializers.CharField(),
        },
    ),
    description='Error estándar de la API',
)

SUBTASK_PATCH_EXAMPLES = [
    OpenApiExample(
        'Posponer (estado + nota opcional)',
        value={'status': 'postponed', 'note': 'Esperando datos del cliente'},
        request_only=True,
    ),
    OpenApiExample(
        'Reprogramar (solo fecha y horas)',
        value={'target_date': '2026-05-20', 'estimated_hours': 2.5},
        request_only=True,
    ),
    OpenApiExample(
        'Actualizar solo nota (ej. desde UI de notas)',
        value={'note': 'Texto actualizado'},
        request_only=True,
    ),
    OpenApiExample(
        'Reprogramar y volver a no pospuesta',
        value={
            'target_date': '2026-05-20',
            'estimated_hours': 2.5,
            'status': 'pending',
        },
        request_only=True,
    ),
    OpenApiExample(
        'Marcar hecho (sin tocar la nota)',
        value={'status': 'done'},
        request_only=True,
    ),
]

activity_list_schema = extend_schema(
    tags=['Actividades'],
    summary='Listar actividades del usuario',
    responses={
        200: inline_serializer(
            name='ActivityListResponse',
            fields={
                'count': serializers.IntegerField(),
                'results': ActivityListSerializer(many=True),
            },
        ),
        401: ERROR_RESPONSE,
    },
)

activity_create_schema = extend_schema(
    tags=['Actividades'],
    summary='Crear actividad',
    request=ActivityDetailSerializer,
    responses={201: ActivityDetailSerializer, 400: ERROR_RESPONSE},
)

activity_detail_get_schema = extend_schema(
    tags=['Actividades'],
    summary='Detalle de actividad con subtareas y progreso',
    responses={200: ActivityDetailSerializer, 401: ERROR_RESPONSE, 404: ERROR_RESPONSE},
)

activity_detail_patch_schema = extend_schema(
    tags=['Actividades'],
    summary='Actualizar actividad (parcial)',
    request=ActivityDetailSerializer,
    responses={200: ActivityDetailSerializer, 400: ERROR_RESPONSE, 404: ERROR_RESPONSE},
)

activity_detail_delete_schema = extend_schema(
    tags=['Actividades'],
    summary='Eliminar actividad',
    responses={204: None, 404: ERROR_RESPONSE},
)

subtask_create_schema = extend_schema(
    tags=['Subtareas'],
    summary='Crear subtarea',
    request=SubtaskSerializer,
    responses={201: SubtaskSerializer, 400: ERROR_RESPONSE, 404: ERROR_RESPONSE},
)

subtask_patch_schema = extend_schema(
    tags=['Subtareas'],
    summary='Actualizar subtarea (parcial)',
    description=(
        'Estados válidos (`status`): `pending` (no pospuesta / en curso), `postponed` (pospuesta), `done` (hecha). '
        '**Posponer:** `status=postponed` y `note` opcional. '
        '**Reprogramar:** `target_date` y/o `estimated_hours`. Para sacar una subtarea '
        'del listado «pospuestas» del cliente sin borrar la nota, también enviar `status=pending`. '
        '**Marcar hecho:** `status=done`. '
        'Si omites `note`, la nota guardada no se borra.'
    ),
    request=SubtaskSerializer,
    examples=SUBTASK_PATCH_EXAMPLES,
    responses={200: SubtaskSerializer, 400: ERROR_RESPONSE, 404: ERROR_RESPONSE},
)

subtask_delete_schema = extend_schema(
    tags=['Subtareas'],
    summary='Eliminar subtarea',
    responses={204: None, 404: ERROR_RESPONSE},
)
