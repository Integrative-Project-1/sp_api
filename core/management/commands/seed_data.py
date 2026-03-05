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

        if demo_created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created user: {demo_user.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⊘ User already exists: {demo_user.username}')
            )

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

        if test_created:
            test_user.set_password('test123')
            test_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created user: {test_user.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⊘ User already exists: {test_user.username}')
            )

        # Ensure test user has capacity
        test_capacity, test_cap_created = UserCapacity.objects.get_or_create(
            user=test_user,
            defaults={'daily_limit': 8}
        )

        if test_cap_created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created capacity for {test_user.username}: {test_capacity.daily_limit}h')
            )

        self.stdout.write(self.style.SUCCESS('✓ Seed data completed!'))
        self.stdout.write(
            self.style.WARNING('\nMock Users Created:')
        )
        self.stdout.write('  - demo / demo123 (6h capacity)')
        self.stdout.write('  - test / test123 (8h capacity)')
