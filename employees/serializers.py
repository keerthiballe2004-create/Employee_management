from rest_framework import serializers
from .models import Department, Role, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        department = data.get(
            'department',
            self.instance.department if self.instance else None
        )

        role = data.get(
            'role',
            self.instance.role if self.instance else None
        )

        if department and role and role.department != department:
            raise serializers.ValidationError({
                'role': 'Selected role does not belong to the selected department.'
            })

        manager = data.get(
            'manager',
            self.instance.manager if self.instance else None
        )

        employee_id = data.get(
            'employee_id',
            self.instance.employee_id if self.instance else None
        )

        if manager and employee_id and manager.employee_id == employee_id:
            raise serializers.ValidationError({
                'manager': 'An employee cannot be their own manager.'
            })

        return data

    class Meta:
        model = Employee
        fields = '__all__'