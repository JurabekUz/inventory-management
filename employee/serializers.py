from rest_framework import serializers
from rest_framework.fields import UUIDField, CharField

from .models import Position, Employee


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'full_name', 'code', 'created_at')
        extra_kwargs = {'code': {'read_only': True}}


class EmployeeSerializer(serializers.ModelSerializer):
    department__name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    position__name = serializers.CharField(source='position.name', read_only=True, allow_null=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'department', 'position', 'department__name', 'position__name',
            'from_date', 'to_date', 'created_at'
        )


class EmployeeShortSerializer(serializers.Serializer):
    id = UUIDField()
    name = CharField()

# class EmployeeListSerializer(serializers.ModelSerializer):
#     department__name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
#     position__name = serializers.CharField(source='position.name', read_only=True, allow_null=True)
#
#     class Meta:
#         model = Employee
#         fields = ['id', 'name', 'department', 'position', 'from_date', 'to_date']
