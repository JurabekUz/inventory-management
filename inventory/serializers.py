from rest_framework.fields import CharField, UUIDField
from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField

from common.serializers import InventoryGroupSerializer, InventoryTypeSerializer, MeasureUnitSerializer
from contract.views import ContractSerializer
from employee.serializers import EmployeeShortSerializer
from inventory.models import Inventory
from stocktaking.models import Stocktaking


class LastStocktakingSerializer(ModelSerializer):
    employee = EmployeeShortSerializer()

    class Meta:
        model = Stocktaking
        fields = ['id', 'number', 'employee', 'date']


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ['organization', 'is_active']
        extra_kwargs = {'code': {'read_only': True}}


class InventoryListSerializer(ModelSerializer):
    group = CharField(source='group.name', read_only=True)
    type = CharField(source='type.name', read_only=True)

    class Meta:
        model = Inventory
        fields = ('id', 'name', 'code', 'group', 'type', 'amount', 'measure_unit', 'date')


class InventoryRetrieveSerializer(ModelSerializer):
    group = InventoryGroupSerializer()
    type = InventoryTypeSerializer()
    contract = ContractSerializer()
    measure_unit = MeasureUnitSerializer()

    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        rep_data = super().to_representation(instance)
        actual_stock = instance.stocktakings.filter(
                terminate_date__isnull=True
            ).select_related('employee').first()
        rep_data['actual_stock'] = LastStocktakingSerializer(actual_stock).data if actual_stock else None
        return rep_data


class InventoryShortSerializer(Serializer):
    id = UUIDField()
    name = CharField()
    code = CharField()
