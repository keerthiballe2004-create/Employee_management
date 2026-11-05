from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    RoleViewSet,
    EmployeeViewSet,
    employees_page
)

router = DefaultRouter()

router.register('departments', DepartmentViewSet)
router.register('roles', RoleViewSet)
router.register('employees', EmployeeViewSet)

urlpatterns = [
    path('employees/ui/', employees_page, name='employees_page'),
] + router.urls