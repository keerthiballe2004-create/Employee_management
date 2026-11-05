from django.contrib import admin
from .models import OffboardingCase


@admin.register(OffboardingCase)
class OffboardingCaseAdmin(admin.ModelAdmin):
    list_display = (
        'offboarding_id',
        'employee',
        'exit_date',
        'status',
        'created_at'
    )

    list_filter = ('status', 'exit_date')

    search_fields = (
        'offboarding_id',
        'employee__first_name',
        'employee__last_name'
    )