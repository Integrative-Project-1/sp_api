from rest_framework import serializers
from .models import Activity, Subtask
from .progress import progress_from_subtasks


class SubtaskSerializer(serializers.ModelSerializer):
    """
    Subtarea: estados pending | done | postponed.
    PATCH parcial: si no envías ``note``, la nota existente se conserva (C1).
    """
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
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'note': {'required': False, 'allow_blank': True},
            'status': {
                'help_text': 'pending | done | postponed. Posponer: postponed + note opcional.',
            },
        }

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request is not None and 'note' not in request.data:
            validated_data.pop('note', None)
        return super().update(instance, validated_data)


class ActivityProgressMixin:
    """Campos de progreso por actividad (C2)."""
    subtasks_done = serializers.SerializerMethodField()
    subtasks_total = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    def get_subtasks_done(self, obj):
        return progress_from_subtasks(obj.subtasks.all())['subtasks_done']

    def get_subtasks_total(self, obj):
        return progress_from_subtasks(obj.subtasks.all())['subtasks_total']

    def get_progress_percent(self, obj):
        return progress_from_subtasks(obj.subtasks.all())['progress_percent']


class ActivityListSerializer(ActivityProgressMixin, serializers.ModelSerializer):
    """Serializer liviano para la lista — sin subtareas anidadas."""
    activity_type_display = serializers.CharField(
        source='get_activity_type_display', read_only=True
    )
    subtask_count = serializers.SerializerMethodField()
    subtasks_done = serializers.SerializerMethodField()
    subtasks_total = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_type', 'activity_type_display',
            'course', 'event_date', 'deadline',
            'subtask_count', 'subtasks_done', 'subtasks_total', 'progress_percent',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subtask_count(self, obj):
        return obj.subtasks.count()


class ActivityDetailSerializer(ActivityListSerializer):
    """Serializer completo para detalle y respuesta de create/update."""
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta(ActivityListSerializer.Meta):
        fields = ActivityListSerializer.Meta.fields + ['subtasks']
