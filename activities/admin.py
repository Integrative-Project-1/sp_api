from django.contrib import admin
from .models import Activity, Subtask, DailyCapacityConfig


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'activity_type', 'deadline', 'user']
    list_filter = ['activity_type', 'course']
    search_fields = ['title', 'course']


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'activity', 'target_date', 'estimated_hours', 'status']
    list_filter = ['status', 'activity']


@admin.register(DailyCapacityConfig)
class DailyCapacityConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_limit']
