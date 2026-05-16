from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from core.responses import validation_error_response
from .models import Activity, Subtask
from .serializers import ActivityListSerializer, ActivityDetailSerializer, SubtaskSerializer
from .openapi import (
    activity_list_schema,
    activity_create_schema,
    activity_detail_get_schema,
    activity_detail_patch_schema,
    activity_detail_delete_schema,
    subtask_create_schema,
    subtask_patch_schema,
    subtask_delete_schema,
)


class ActivityListCreateView(APIView):
    """
    GET  /api/activities/   Lista actividades del usuario autenticado.
    POST /api/activities/   Crea una nueva actividad.
    """

    @activity_list_schema
    def get(self, request):
        activities = Activity.objects.filter(user=request.user).prefetch_related('subtasks')
        serializer = ActivityListSerializer(activities, many=True)
        return Response({'count': len(serializer.data), 'results': serializer.data})

    @activity_create_schema
    def post(self, request):
        serializer = ActivityDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return validation_error_response(serializer)


class ActivityDetailView(APIView):
    """
    GET    /api/activities/{id}/   Detalle con subtareas anidadas.
    PATCH  /api/activities/{id}/   Actualización parcial.
    DELETE /api/activities/{id}/   Elimina actividad y subtareas (CASCADE).
    """

    def get_object(self, pk, user):
        try:
            return Activity.objects.prefetch_related('subtasks').get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()

    @activity_detail_get_schema
    def get(self, request, pk):
        activity = self.get_object(pk, request.user)
        return Response(ActivityDetailSerializer(activity).data)

    @activity_detail_patch_schema
    def patch(self, request, pk):
        activity = self.get_object(pk, request.user)
        serializer = ActivityDetailSerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return validation_error_response(serializer)

    @activity_detail_delete_schema
    def delete(self, request, pk):
        activity = self.get_object(pk, request.user)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubtaskListCreateView(APIView):
    """
    POST /api/activities/{id}/subtasks/   Crea subtarea para una actividad.
    """

    def get_activity(self, pk, user):
        try:
            return Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()

    @subtask_create_schema
    def post(self, request, pk):
        activity = self.get_activity(pk, request.user)
        serializer = SubtaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(activity=activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return validation_error_response(serializer)


class SubtaskDetailView(APIView):
    """
    PATCH  /api/activities/{id}/subtasks/{subtask_id}/   Actualización parcial.
    DELETE /api/activities/{id}/subtasks/{subtask_id}/   Elimina subtarea.
    """

    def get_object(self, pk, subtask_id, user):
        try:
            activity = Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()
        try:
            return Subtask.objects.get(pk=subtask_id, activity=activity)
        except Subtask.DoesNotExist:
            raise NotFound()

    @subtask_patch_schema
    def patch(self, request, pk, subtask_id):
        subtask = self.get_object(pk, subtask_id, request.user)
        serializer = SubtaskSerializer(
            subtask,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return validation_error_response(serializer)

    @subtask_delete_schema
    def delete(self, request, pk, subtask_id):
        subtask = self.get_object(pk, subtask_id, request.user)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
