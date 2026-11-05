from django.db import models
from employees.models import Employee


class OnboardingCase(models.Model):

    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]

    onboarding_id = models.CharField(
        max_length=20,
        primary_key=True
    )

    employee = models.ForeignKey(
     Employee,
     on_delete=models.PROTECT,
     related_name="onboarding_cases"
    )

    start_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.onboarding_id