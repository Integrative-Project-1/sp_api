from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    SubtaskListCreateView,
    SubtaskDetailView,
)

urlpatterns = [
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('<int:pk>/subtasks/', SubtaskListCreateView.as_view(), name='subtask-list-create'),
    path('<int:pk>/subtasks/<int:subtask_id>/', SubtaskDetailView.as_view(), name='subtask-detail'),
]
