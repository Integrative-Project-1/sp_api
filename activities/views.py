from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound

from .models import Activity, Subtask
from .serializers import ActivityListSerializer, ActivityDetailSerializer, SubtaskSerializer

User = get_user_model()


class ServiceUnavailable(APIException):
    status_code = 503
    default_code = 'service_unavailable'


def get_demo_user():
    """Retorna el usuario demo. Lanza 503 si no existe (ejecutar seed_data)."""
    try:
        return User.objects.get(username='demo')
    except User.DoesNotExist:
        raise ServiceUnavailable(
            detail="Usuario demo no disponible. Ejecute: python manage.py seed_data"
        )


class ActivityListCreateView(APIView):
    """
    GET  /api/activities/   Lista actividades del usuario demo.
    POST /api/activities/   Crea una nueva actividad.
    """

    def get(self, request):
        user = get_demo_user()
        activities = Activity.objects.filter(user=user)
        serializer = ActivityListSerializer(activities, many=True)
        return Response({'count': len(serializer.data), 'results': serializer.data})

    def post(self, request):
        user = get_demo_user()
        serializer = ActivityDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetailView(APIView):
    """
    GET    /api/activities/{id}/   Detalle con subtareas anidadas.
    PATCH  /api/activities/{id}/   Actualización parcial.
    DELETE /api/activities/{id}/   Elimina actividad y subtareas (CASCADE).
    """

    def get_object(self, pk):
        user = get_demo_user()
        try:
            return Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        activity = self.get_object(pk)
        return Response(ActivityDetailSerializer(activity).data)

    def patch(self, request, pk):
        activity = self.get_object(pk)
        serializer = ActivityDetailSerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubtaskListCreateView(APIView):
    """
    POST /api/activities/{id}/subtasks/   Crea subtarea para una actividad.
    """

    def get_activity(self, pk):
        user = get_demo_user()
        try:
            return Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()

    def post(self, request, pk):
        activity = self.get_activity(pk)
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(activity=activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtaskDetailView(APIView):
    """
    PATCH  /api/activities/{id}/subtasks/{subtask_id}/   Actualización parcial.
    DELETE /api/activities/{id}/subtasks/{subtask_id}/   Elimina subtarea.
    """

    def get_object(self, pk, subtask_id):
        user = get_demo_user()
        try:
            activity = Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            raise NotFound()
        try:
            return Subtask.objects.get(pk=subtask_id, activity=activity)
        except Subtask.DoesNotExist:
            raise NotFound()

    def patch(self, request, pk, subtask_id):
        subtask = self.get_object(pk, subtask_id)
        serializer = SubtaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, subtask_id):
        subtask = self.get_object(pk, subtask_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
