from django.db import models
from employees.models import Employee


class OffboardingCase(models.Model):

    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('APPROVAL_PENDING', 'Approval Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]

    offboarding_id = models.CharField(
        max_length=20,
        primary_key=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='offboarding_cases'
    )

    exit_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REQUESTED'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.offboarding_id