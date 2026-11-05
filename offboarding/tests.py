
from django.test import TestCase
from rest_framework import serializers

from employees.models import Employee, Department, Role
from offboarding.models import OffboardingCase
from offboarding.serializers import OffboardingCaseSerializer
from tasks.models import Task
from assets.models import Asset, AssetAssignment


class OffboardingTest(TestCase):

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
            email="offboardingtest@example.com",
            department=self.department,
            role=self.role,
            hire_date="2026-11-04",
            employment_status="ACTIVE"
        )

    def test_offboarding_creates_three_tasks(self):

        serializer = OffboardingCaseSerializer(data={
            "offboarding_id": "OFFTEST",
            "employee": self.employee.pk,
            "exit_date": "2026-11-25",
            "reason": "Personal reasons",
            "status": "REQUESTED"
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)

        offboarding = serializer.save()

        self.assertEqual(offboarding.offboarding_id, "OFFTEST")

        self.assertEqual(
            Task.objects.filter(employee=self.employee).count(),
            3
        )

        self.assertTrue(
            Task.objects.filter(task_id="OFFTEST-HR").exists()
        )

        self.assertTrue(
            Task.objects.filter(task_id="OFFTEST-IT").exists()
        )

        self.assertTrue(
            Task.objects.filter(task_id="OFFTEST-FAC").exists()
        )

    def test_terminated_employee_cannot_be_offboarded(self):

        self.employee.employment_status = "TERMINATED"
        self.employee.save()

        serializer = OffboardingCaseSerializer(data={
            "offboarding_id": "OFFTEST2",
            "employee": self.employee.pk,
            "exit_date": "2026-11-25",
            "reason": "Personal reasons",
            "status": "REQUESTED"
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_duplicate_active_offboarding_is_rejected(self):

        OffboardingCase.objects.create(
            offboarding_id="OFFTEST3",
            employee=self.employee,
            exit_date="2026-11-25",
            reason="Personal reasons",
            status="REQUESTED"
        )

        serializer = OffboardingCaseSerializer(data={
            "offboarding_id": "OFFTEST4",
            "employee": self.employee.pk,
            "exit_date": "2026-12-01",
            "reason": "Another request",
            "status": "REQUESTED"
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_offboarding_cannot_complete_with_unreturned_assets(self):

        offboarding = OffboardingCase.objects.create(
            offboarding_id="OFFTEST5",
            employee=self.employee,
            exit_date="2026-11-25",
            reason="Personal reasons",
            status="REQUESTED"
        )

        asset = Asset.objects.create(
            asset_id="ASTTEST",
            asset_name="Test Laptop",
            asset_type="LAPTOP",
            serial_number="TESTSERIAL001",
            purchase_date="2026-10-15",
            status="ASSIGNED"
        )

        AssetAssignment.objects.create(
            assignment_id="ASNTEST",
            asset=asset,
            employee=self.employee,
            assigned_date="2026-11-04",
            condition_on_assignment="GOOD",
            is_returned=False
        )

        serializer = OffboardingCaseSerializer(
            offboarding,
            data={"status": "COMPLETED"},
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        with self.assertRaises(serializers.ValidationError):
            serializer.save()

        offboarding.refresh_from_db()

        self.assertEqual(offboarding.status, "REQUESTED")

    def test_employee_is_terminated_after_offboarding_completion(self):

        offboarding = OffboardingCase.objects.create(
            offboarding_id="OFFTEST6",
            employee=self.employee,
            exit_date="2026-11-25",
            reason="Personal reasons",
            status="IN_PROGRESS"
        )

        serializer = OffboardingCaseSerializer(
            offboarding,
            data={"status": "COMPLETED"},
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.employee.refresh_from_db()

        self.assertEqual(
            self.employee.employment_status,
            "TERMINATED"
        )
