
from django.test import TestCase

from employees.models import Employee, Department, Role
from onboarding.models import OnboardingCase
from onboarding.serializers import OnboardingCaseSerializer
from tasks.models import Task


class OnboardingTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            department_id="D001",
            department_name="Testing"
        )

        self.role = Role.objects.create(
            role_id="R001",
            role_name="Python Developer",
            department=self.department
        )

        self.employee = Employee.objects.create(
            employee_id="EMPTEST",
            first_name="Test",
            last_name="Employee",
            email="onboardingtest@example.com",
            department=self.department,
            role=self.role,
            hire_date="2026-11-04",
            employment_status="ACTIVE"
        )

    def test_onboarding_creates_three_tasks(self):

        serializer = OnboardingCaseSerializer(data={
            "onboarding_id": "ONBTEST",
            "employee": self.employee.pk,
            "start_date": "2026-11-10",
            "status": "NOT_STARTED"
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)

        onboarding = serializer.save()

        self.assertEqual(onboarding.onboarding_id, "ONBTEST")
        self.assertEqual(
            Task.objects.filter(employee=self.employee).count(),
            3
        )

        self.assertTrue(
            Task.objects.filter(task_id="ONBTEST-HR").exists()
        )

        self.assertTrue(
            Task.objects.filter(task_id="ONBTEST-IT").exists()
        )

        self.assertTrue(
            Task.objects.filter(task_id="ONBTEST-FAC").exists()
        )
    def test_terminated_employee_cannot_be_onboarded(self):

        self.employee.employment_status = "TERMINATED"
        self.employee.save()

        serializer = OnboardingCaseSerializer(data={
            "onboarding_id": "ONBTEST2",
            "employee": self.employee.pk,
            "start_date": "2026-11-10",
            "status": "NOT_STARTED"
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        
    def test_duplicate_active_onboarding_is_rejected(self):

        OnboardingCase.objects.create(
            onboarding_id="ONBTEST3",
            employee=self.employee,
            start_date="2026-11-10",
            status="IN_PROGRESS"
        )

        serializer = OnboardingCaseSerializer(data={
            "onboarding_id": "ONBTEST4",
            "employee": self.employee.pk,
            "start_date": "2026-11-15",
            "status": "NOT_STARTED"
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


        