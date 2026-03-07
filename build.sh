#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data
python manage.py shell -c "
from core.models import User
for username, password in [('demo','demo123'),('test','test123'),('student','study2024')]:
    try:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print('Password reset:', username)
    except User.DoesNotExist:
        print('User not found:', username)
"
