from datetime import date
from rest_framework import serializers
from .models import OffboardingCase
from access_management.models import Access
from assets.models import AssetAssignment
from tasks.models import Task


class OffboardingCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = OffboardingCase
        fields = '__all__'

    def validate(self, data):

        employee = data.get(
            'employee',
            self.instance.employee if self.instance else None
        )

        if employee and employee.employment_status == 'TERMINATED':
            raise serializers.ValidationError(
                "Cannot create an offboarding case for an already terminated employee."
            )

        if employee:
            existing_cases = OffboardingCase.objects.filter(
                employee=employee
            ).exclude(status='COMPLETED')

            if self.instance:
                existing_cases = existing_cases.exclude(
                    offboarding_id=self.instance.offboarding_id
                )

            if existing_cases.exists():
                raise serializers.ValidationError(
                    "This employee already has an active offboarding case."
                )

        return data

    def create(self, validated_data):

        offboarding = super().create(validated_data)

        employee = offboarding.employee

        # Automatically create HR task
        Task.objects.create(
            task_id=f"{offboarding.offboarding_id}-HR",
            employee=employee,
            task_name="Conduct Exit Interview",
            description="Conduct the employee exit interview and collect feedback.",
            department="HR",
            assigned_to="HR Manager",
            due_date=offboarding.exit_date,
            priority="HIGH"
        )

        # Automatically create IT task
        Task.objects.create(
            task_id=f"{offboarding.offboarding_id}-IT",
            employee=employee,
            task_name="Review and Revoke System Access",
            description="Review employee system access and revoke it during offboarding.",
            department="IT",
            assigned_to="IT Administrator",
            due_date=offboarding.exit_date,
            priority="HIGH"
        )

        # Automatically create Facilities task
        Task.objects.create(
            task_id=f"{offboarding.offboarding_id}-FAC",
            employee=employee,
            task_name="Collect Company Assets",
            description="Collect laptop, ID card and other company-issued equipment.",
            department="FACILITIES",
            assigned_to="Facilities Manager",
            due_date=offboarding.exit_date,
            priority="HIGH"
        )

        return offboarding

    def update(self, instance, validated_data):

        new_status = validated_data.get('status', instance.status)

        # Check outstanding assets before completing offboarding
        if new_status == 'COMPLETED':

            outstanding_assets = AssetAssignment.objects.filter(
                employee=instance.employee,
                is_returned=False
            ).select_related('asset')

            if outstanding_assets.exists():

                asset_names = [
                    assignment.asset.asset_name
                    for assignment in outstanding_assets
                ]

                raise serializers.ValidationError({
                    'assets': (
                        'Offboarding cannot be completed. '
                        'The employee must return these assets: '
                        + ', '.join(asset_names)
                    )
                })

        instance = super().update(instance, validated_data)

        if instance.status == 'COMPLETED':

            employee = instance.employee

            # Update employee status
            employee.employment_status = 'TERMINATED'
            employee.save(update_fields=['employment_status'])

            # Revoke all active system access
            Access.objects.filter(
                employee=employee,
                status='ACTIVE'
            ).update(
                status='REVOKED',
                revoked_date=date.today()
            )

        return instance