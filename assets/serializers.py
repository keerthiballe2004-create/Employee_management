from datetime import date
from rest_framework import serializers
from .models import Asset, AssetAssignment


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class AssetAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetAssignment
        fields = '__all__'

    def validate(self, data):
        asset = data.get(
            'asset',
            self.instance.asset if self.instance else None
        )

        employee = data.get(
            'employee',
            self.instance.employee if self.instance else None
        )

        if employee and employee.employment_status == 'TERMINATED':
            raise serializers.ValidationError(
                "Cannot assign assets to terminated employees."
            )

        if self.instance is None and asset.status != 'AVAILABLE':
            raise serializers.ValidationError(
                "This asset is not available for assignment."
            )

        if self.instance is not None and asset != self.instance.asset:
            if asset.status != 'AVAILABLE':
                raise serializers.ValidationError(
                    "The selected asset is not available."
                )

        return data

    def create(self, validated_data):
        assignment = super().create(validated_data)

        asset = assignment.asset
        asset.status = 'ASSIGNED'
        asset.save(update_fields=['status'])

        return assignment

    def update(self, instance, validated_data):
        is_returned = validated_data.get(
            'is_returned',
            instance.is_returned
        )

        if is_returned and not instance.is_returned:
            validated_data['returned_date'] = (
                validated_data.get('returned_date') or date.today()
            )

        assignment = super().update(instance, validated_data)

        if assignment.is_returned:
            asset = assignment.asset
            asset.status = 'AVAILABLE'
            asset.save(update_fields=['status'])

        return assignment