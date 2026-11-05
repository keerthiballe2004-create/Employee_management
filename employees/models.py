from django.db import models


class Department(models.Model):
    department_id = models.CharField(
        max_length=10,
        primary_key=True
    )
    department_name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.department_name


class Role(models.Model):
    role_id = models.CharField(
        max_length=10,
        primary_key=True
    )
    role_name = models.CharField(max_length=100)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='roles'
    )

    def __str__(self):
        return self.role_name


class Employee(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ON_LEAVE', 'On Leave'),
        ('TERMINATED', 'Terminated'),
    ]

    employee_id = models.CharField(
        max_length=15,
        primary_key=True
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    hire_date = models.DateField()

    employment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    is_contractor = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name}"