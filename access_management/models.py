from django.db import models
from employees.models import Employee


class Access(models.Model):

    ACCESS_STATUS = [
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved'),
        ('ACTIVE', 'Active'),
        ('REVOKED', 'Revoked'),
        ('REJECTED', 'Rejected'),
    ]

    access_id = models.CharField(
        max_length=20,
        primary_key=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='system_access'
    )

    system_name = models.CharField(max_length=100)

    access_level = models.CharField(max_length=100)

    requested_by = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=ACCESS_STATUS,
        default='REQUESTED'
    )

    requested_date = models.DateField()

    approved_date = models.DateField(
        null=True,
        blank=True
    )

    revoked_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.access_id