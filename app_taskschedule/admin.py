from django.contrib import admin
from .models import TaskSchedule

# Register your models here.

@admin.register(TaskSchedule)
class TaskScheduleAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'day_of_week', 'hour', 'minute']
    list_editable = ['day_of_week', 'hour', 'minute']

