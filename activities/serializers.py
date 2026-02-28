from rest_framework import serializers
from .models import Activity, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = Subtask
        fields = [
            'id', 'name', 'target_date', 'estimated_hours',
            'status', 'status_display', 'note',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
        # status es read_only en Sprint 1 — los cambios de estado son US-09 (Sprint 4)


class ActivityListSerializer(serializers.ModelSerializer):
    """Serializer liviano para la lista — sin subtareas anidadas."""
    activity_type_display = serializers.CharField(
        source='get_activity_type_display', read_only=True
    )
    subtask_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_type', 'activity_type_display',
            'course', 'event_date', 'deadline',
            'subtask_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subtask_count(self, obj):
        return obj.subtasks.count()


class ActivityDetailSerializer(ActivityListSerializer):
    """Serializer completo para detalle y respuesta de create/update."""
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta(ActivityListSerializer.Meta):
        fields = ActivityListSerializer.Meta.fields + ['subtasks']
