from rest_framework import viewsets
from django.shortcuts import render

from .models import Department, Role, Employee

from .serializers import (
    DepartmentSerializer,
    RoleSerializer,
    EmployeeSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.select_related(
        'department', 'role', 'manager'
    ).all().order_by('employee_id')

    serializer_class = EmployeeSerializer

    filterset_fields = [
        'department',
        'role',
        'employment_status',
        'is_contractor'
    ]

    search_fields = [
        'employee_id',
        'first_name',
        'last_name',
        'email'
    ]

    ordering_fields = [
        'first_name',
        'hire_date',
        'employee_id'
    ]

def employees_page(request):
    return render(request, 'employees/employees.html')