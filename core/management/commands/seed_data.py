from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import UserCapacity

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with mock users for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting seed data...'))

        # Mock User 1: demo
        demo_user, demo_created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )

        demo_user.set_password('demo123')
        demo_user.save()
        action = 'Created' if demo_created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'+ {action} user: {demo_user.username}'))

        # Ensure demo user has capacity
        demo_capacity, demo_cap_created = UserCapacity.objects.get_or_create(
            user=demo_user,
            defaults={'daily_limit': 6}
        )

        if demo_cap_created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created capacity for {demo_user.username}: {demo_capacity.daily_limit}h')
            )

        # Mock User 2: test
        test_user, test_created = User.objects.get_or_create(
            username='test',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )

        test_user.set_password('test123')
        test_user.save()
        action = 'Created' if test_created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'+ {action} user: {test_user.username}'))

        # Ensure test user has capacity
        test_capacity, test_cap_created = UserCapacity.objects.get_or_create(
            user=test_user,
            defaults={'daily_limit': 8}
        )

        if test_cap_created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created capacity for {test_user.username}: {test_capacity.daily_limit}h')
            )

        # User 3: student
        student_user, student_created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@studyplan.com',
                'first_name': 'Study',
                'last_name': 'Student',
            }
        )
        student_user.set_password('study2024')
        student_user.save()
        action = 'Created' if student_created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'+ {action} user: {student_user.username}'))

        UserCapacity.objects.get_or_create(
            user=student_user,
            defaults={'daily_limit': 6}
        )

        self.stdout.write(self.style.SUCCESS('+ Seed data completed!'))
        self.stdout.write('  - demo / demo123')
        self.stdout.write('  - test / test123')
        self.stdout.write('  - student / study2024')
