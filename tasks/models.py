from django.db import models
from employees.models import Employee


class Task(models.Model):

    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('FACILITIES', 'Facilities'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('BLOCKED', 'Blocked'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    task_id = models.CharField(max_length=20, primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='lifecycle_tasks'
    )
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES
    )
    assigned_to = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_id