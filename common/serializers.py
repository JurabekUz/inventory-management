from rest_framework import serializers

from . import models


class IdNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'code', 'created_at']
        extra_kwargs = {
            'code': {'read_only': True}
        }


class InventoryGroupSerializer(serializers.ModelSerializer):
    parent__name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)

    class Meta:
        model = models.InventoryGroup
        fields = ['id', 'name', 'parent', 'parent__name', 'code', 'created_at']
        extra_kwargs = {
            'code': {'read_only': True}
        }


class InventoryGroupDetailSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.InventoryGroup
        fields = ['id', 'name', 'parent', 'children', 'code', 'created_at']

    def get_children(self, obj):
        return obj.children.all().values('id', 'name')



class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventoryType
        fields = ['id', 'name', 'code', 'created_at']
        extra_kwargs = {
            'code': {'read_only': True}
        }


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MeasureUnit
        fields = ['id', 'name', 'number_type', 'created_at']
