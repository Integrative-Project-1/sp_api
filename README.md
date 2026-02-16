# Study Planner API

Backend with Django REST Framework.

## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment: `cp .env.example .env` and edit with Supabase credentials
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Seed data (optional): `python manage.py seed_data`
8. Run server: `python manage.py runserver`

**API**: http://localhost:8000
**Admin**: http://localhost:8000/admin
**Health Check**: http://localhost:8000/api/health/

## Deployment

**Production**: https://<your-app>.onrender.com/api/
**Admin**: https://<your-app>.onrender.com/admin/
