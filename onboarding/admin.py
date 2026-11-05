
from django.contrib import admin
from .models import OnboardingCase


@admin.register(OnboardingCase)
class OnboardingCaseAdmin(admin.ModelAdmin):

    list_display = (
        'onboarding_id',
        'employee',
        'start_date',
        'status',
        'created_at'
    )

    list_filter = ('status', 'start_date')

    search_fields = (
        'onboarding_id',
        'employee__first_name',
        'employee__last_name'
    )
