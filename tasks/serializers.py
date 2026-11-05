from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):

        new_status = data.get(
            'status',
            self.instance.status if self.instance else 'PENDING'
        )

        old_status = self.instance.status if self.instance else None

        if old_status == 'BLOCKED' and new_status == 'COMPLETED':
            raise serializers.ValidationError(
                "A blocked task must be moved to IN_PROGRESS before completion."
            )

        return data