#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from core.models import User, UserCapacity
users = [
    ('demo',    'demo123',    'demo@example.com'),
    ('test',    'test123',    'test@example.com'),
    ('student', 'study2024',  'student@studyplan.com'),
]
for username, password, email in users:
    u, created = User.objects.get_or_create(username=username)
    u.email = email
    u.set_password(password)
    u.save()
    UserCapacity.objects.get_or_create(user=u, defaults={'daily_limit': 6})
    print(('Created' if created else 'Updated') + ': ' + username)
print('Done')
"
