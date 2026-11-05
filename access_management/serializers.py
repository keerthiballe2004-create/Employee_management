from rest_framework import serializers
from .models import Access


class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = '__all__'

    def validate(self, data):
        employee = data.get(
            'employee',
            self.instance.employee if self.instance else None
        )

        if employee and employee.employment_status == 'TERMINATED':
            raise serializers.ValidationError(
                "Terminated employees cannot receive system access."
            )

        return data

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        if new_status == 'ACTIVE' and instance.status != 'APPROVED':
            raise serializers.ValidationError(
                "Access must be approved before it can become active."
            )

        if new_status == 'APPROVED':
            validated_data['approved_date'] = (
                validated_data.get('approved_date')
                or instance.approved_date
                or __import__('datetime').date.today()
            )

        if new_status == 'REVOKED':
            validated_data['revoked_date'] = (
                validated_data.get('revoked_date')
                or instance.revoked_date
                or __import__('datetime').date.today()
            )

        return super().update(instance, validated_data)