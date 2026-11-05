
from django.test import TestCase

from employees.models import Employee, Department, Role
from employees.serializers import EmployeeSerializer


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.department1 = Department.objects.create(
            department_id="D001",
            department_name="Testing"
        )

        self.department2 = Department.objects.create(
            department_id="D002",
            department_name="Development"
        )

        self.role1 = Role.objects.create(
            role_id="R001",
            role_name="Python Developer",
            department=self.department1
        )

        self.role2 = Role.objects.create(
            role_id="R002",
            role_name="Java Developer",
            department=self.department2
        )

    def test_employee_creation(self):
        employee = Employee.objects.create(
            employee_id="EMPTEST",
            first_name="Test",
            last_name="Employee",
            email="testemployee@example.com",
            department=self.department1,
            role=self.role1,
            hire_date="2026-11-04",
            employment_status="ACTIVE"
        )

        self.assertEqual(employee.employee_id, "EMPTEST")
        self.assertEqual(employee.employment_status, "ACTIVE")

    def test_role_must_belong_to_department(self):
        serializer = EmployeeSerializer(data={
            "employee_id": "EMPTEST2",
            "first_name": "Test",
            "last_name": "Employee",
            "email": "testemployee2@example.com",
            "department": self.department1.pk,
            "role": self.role2.pk,
            "hire_date": "2026-11-04",
            "employment_status": "ACTIVE",
            "is_contractor": False,
            "manager": None
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("role", serializer.errors)

    def test_employee_cannot_be_own_manager(self):
        employee = Employee.objects.create(
            employee_id="EMPTEST3",
            first_name="Test",
            last_name="Manager",
            email="testmanager@example.com",
            department=self.department1,
            role=self.role1,
            hire_date="2026-11-04",
            employment_status="ACTIVE"
        )

        serializer = EmployeeSerializer(
            employee,
            data={"manager": employee.pk},
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("manager", serializer.errors)
