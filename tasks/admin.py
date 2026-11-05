from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'task_id',
        'task_name',
        'employee',
        'department',
        'assigned_to',
        'due_date',
        'status',
        'priority'
    )

    list_filter = (
        'department',
        'status',
        'priority'
    )

    search_fields = (
        'task_id',
        'task_name',
        'assigned_to'
    )