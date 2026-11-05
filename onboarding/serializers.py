

from rest_framework import serializers
from .models import OnboardingCase
from tasks.models import Task


class OnboardingCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnboardingCase
        fields = '__all__'

    def validate(self, data):

        employee = data.get(
            'employee',
            self.instance.employee if self.instance else None
        )

        if employee and employee.employment_status == 'TERMINATED':
            raise serializers.ValidationError(
                "Cannot create an onboarding case for an already terminated employee."
            )

        if employee:
            existing_cases = OnboardingCase.objects.filter(
                employee=employee
            ).exclude(status='COMPLETED')

            if self.instance:
                existing_cases = existing_cases.exclude(
                    onboarding_id=self.instance.onboarding_id
                )

            if existing_cases.exists():
                raise serializers.ValidationError(
                    "This employee already has an active onboarding case."
                )

        return data

    def create(self, validated_data):

        onboarding = super().create(validated_data)

        employee = onboarding.employee

        # Automatically create HR task
        Task.objects.create(
            task_id=f"{onboarding.onboarding_id}-HR",
            employee=employee,
            task_name="Verify Employee Documents",
            description="Verify employee identity and employment documents.",
            department="HR",
            assigned_to="HR Manager",
            due_date=onboarding.start_date,
            priority="HIGH"
        )

        # Automatically create IT task
        Task.objects.create(
            task_id=f"{onboarding.onboarding_id}-IT",
            employee=employee,
            task_name="Create Company Email and System Access",
            description="Set up company email and required system access.",
            department="IT",
            assigned_to="IT Administrator",
            due_date=onboarding.start_date,
            priority="HIGH"
        )

        # Automatically create Facilities task
        Task.objects.create(
            task_id=f"{onboarding.onboarding_id}-FAC",
            employee=employee,
            task_name="Prepare Laptop and Workstation",
            description="Prepare laptop, workstation and other required equipment.",
            department="FACILITIES",
            assigned_to="Facilities Manager",
            due_date=onboarding.start_date,
            priority="MEDIUM"
        )

        return onboarding