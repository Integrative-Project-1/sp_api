from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from activities.models import Activity, Subtask, DailyCapacityConfig
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        # Crear usuario demo
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@example.com', 'first_name': 'Demo', 'last_name': 'User'}
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user'))

        # Configuración de capacidad
        DailyCapacityConfig.objects.get_or_create(user=demo_user, defaults={'daily_limit': 6})

        # Actividad de ejemplo
        activity = Activity.objects.create(
            user=demo_user,
            title='Parcial de Cálculo',
            activity_type='exam',
            course='Cálculo Diferencial',
            deadline=date.today() + timedelta(days=7)
        )

        # Subtareas de ejemplo
        Subtask.objects.create(
            activity=activity,
            name='Repasar derivadas',
            target_date=date.today() + timedelta(days=2),
            estimated_hours=3.0
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
