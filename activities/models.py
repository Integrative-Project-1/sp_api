from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import User


class Activity(models.Model):
    """Actividad evaluativa (examen, quiz, taller, proyecto, etc.)"""
    ACTIVITY_TYPES = [
        ('exam', 'Examen'),
        ('quiz', 'Quiz'),
        ('workshop', 'Taller'),
        ('project', 'Proyecto'),
        ('other', 'Otro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    course = models.CharField(max_length=100)
    event_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['deadline']

    def __str__(self):
        return f"{self.title} - {self.course}"


class Subtask(models.Model):
    """Subtarea de una actividad"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('done', 'Hecho'),
        ('postponed', 'Pospuesto'),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=200)
    target_date = models.DateField()
    estimated_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.1)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['target_date', 'estimated_hours']

    def __str__(self):
        return f"{self.name} ({self.activity.title})"


class DailyCapacityConfig(models.Model):
    """Configuración de capacidad diaria del usuario (US-12)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='capacity_config')
    daily_limit = models.IntegerField(
        default=6,
        validators=[MinValueValidator(1), MaxValueValidator(16)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.daily_limit}h/day"
