from django.db import models
from employees.models import Employee


class Asset(models.Model):

    ASSET_TYPES = [
        ('LAPTOP', 'Laptop'),
        ('MONITOR', 'Monitor'),
        ('KEYBOARD', 'Keyboard'),
        ('MOUSE', 'Mouse'),
        ('ID_CARD', 'ID Card'),
        ('PHONE', 'Mobile Phone'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ASSIGNED', 'Assigned'),
        ('UNDER_MAINTENANCE', 'Under Maintenance'),
        ('RETIRED', 'Retired'),
    ]

    asset_id = models.CharField(max_length=20, primary_key=True)
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    def __str__(self):
        return self.asset_id


class AssetAssignment(models.Model):

    CONDITION_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('DAMAGED', 'Damaged'),
    ]

    assignment_id = models.CharField(max_length=20, primary_key=True)

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name='assignments'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='asset_assignments'
    )

    assigned_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    condition_on_assignment = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='GOOD'
    )

    condition_on_return = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        null=True,
        blank=True
    )

    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return self.assignment_id