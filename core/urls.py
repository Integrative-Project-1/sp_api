from django.urls import path

from .views import (
    login_view,
    logout_view,
    me_view,
    capacity_view,
)

urlpatterns = [
    # Auth endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', me_view, name='me'),
    
    # Capacity endpoints
    path('capacity/', capacity_view, name='capacity'),
]

