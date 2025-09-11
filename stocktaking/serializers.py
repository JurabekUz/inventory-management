from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from employee.serializers import EmployeeShortSerializer
from inventory.serializers import InventoryShortSerializer
from stocktaking.models import Stocktaking, Inspection
from users.serializers import CheckerSerializer


class InspectionListSerializer(ModelSerializer):
    user = CheckerSerializer()

    class Meta:
        model = Inspection
        fields = ['id', 'user', 'created_at']


class StocktakingSerializer(ModelSerializer):
    class Meta:
        model = Stocktaking
        exclude = ('is_active', )
        extra_kwargs = {
            'number': {'read_only': True}
        }

    def validate_inventory(self, value):
        if not value.is_active:
            raise ValidationError('Inventory is not active')
        elif value.stocktakings.filter(terminate_date__isnull=True).exists():
            raise ValidationError('Inventory is already taken')
        return value


class StocktakingListSerializer(ModelSerializer):
    inventory_name = CharField(source='inventory.name', read_only=True)
    inventory_code = CharField(source='inventory.code', read_only=True)
    employee_name = CharField(source='employee.name', read_only=True, allow_null=True)

    class Meta:
        model = Stocktaking
        fields = ['id', 'inventory_name', 'inventory_code', 'number', 'date', 'employee_name']


class StocktakingRetrieveSerializer(ModelSerializer):
    inventory = InventoryShortSerializer()
    employee = EmployeeShortSerializer()
    inspections = InspectionListSerializer(many=True, read_only=True)

    class Meta:
        model = Stocktaking
        fields = '__all__'
