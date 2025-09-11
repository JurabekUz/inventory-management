import django_filters
from employee.models import Employee
from inventory.models import Inventory
from stocktaking.models import Stocktaking


class EmployeeFilter(django_filters.FilterSet):
    is_currently_working = django_filters.BooleanFilter(method='filter_is_currently_working')

    class Meta:
        model = Employee
        fields = {
            'position': ['exact'],
            'department': ['exact'],
            'from_date': ['gte'],
            'to_date': ['lte'],
        }

    def filter_is_currently_working(self, queryset, name, value):
        if value:
            return queryset.filter(from_date__isnull=True)
        return queryset


class InventoryFilter(django_filters.FilterSet):

    class Meta:
        model = Inventory
        fields = {
            'group': ['exact'],
            'type': ['exact'],
            'contract': ['exact'],
            'measure_unit': ['exact'],
            'date': ['gte', 'lte', 'exact'],
            'terminate_date': ['gte', 'lte', 'exact', 'isnull'],
        }


class StocktakingFilter(django_filters.FilterSet):

    class Meta:
        model = Stocktaking
        fields = {
            'inventory': ['exact'],
            'employee': ['exact'],
            'date': ['gte', 'lte', 'exact'],
            'terminate_date': ['gte', 'lte', 'exact', 'isnull'],
        }
