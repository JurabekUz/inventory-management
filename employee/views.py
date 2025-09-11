from rest_framework.viewsets import ModelViewSet

from utils.filters import EmployeeFilter
from utils.mixens import ArchiveMixin, SelectMixin, AutoOrgSetMixin, OrgFilterMixin
from .models import Position, Employee
from .serializers import PositionSerializer, EmployeeSerializer


class PositionViewSet(ArchiveMixin, SelectMixin, AutoOrgSetMixin, OrgFilterMixin, ModelViewSet):
    queryset = Position.objects.filter(is_active=True)
    serializer_class = PositionSerializer
    search_fields = ('name', 'full_name', 'code')


class EmployeeViewSet(ArchiveMixin, SelectMixin, AutoOrgSetMixin, OrgFilterMixin, ModelViewSet):
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer
    search_fields = ('name',)
    filterset_class = EmployeeFilter

