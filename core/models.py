from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom user model. Sprint 0-1: demo user. Sprint 2+: auth completa."""
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class UserCapacity(models.Model):
    """Configuración de capacidad diaria por usuario."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='capacity'
    )
    daily_limit = models.PositiveIntegerField(
        default=6,
        validators=[MinValueValidator(1), MaxValueValidator(16)],
        help_text='Límite de horas de capacidad diaria (1-16 horas)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'user capacity'
        verbose_name_plural = 'user capacities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.daily_limit}h"

