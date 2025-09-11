from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from inventory.models import Inventory
from inventory.serializers import InventorySerializer, InventoryListSerializer, InventoryRetrieveSerializer
from utils.filters import InventoryFilter
from utils.mixens import ArchiveMixin, AutoOrgSetMixin


class InventoryViewSet(ArchiveMixin, AutoOrgSetMixin, ModelViewSet):
    queryset = Inventory.objects.filter(is_active=True)
    serializer_class = InventorySerializer
    search_fields = ('name', 'code', 'full_name')
    filterset_class = InventoryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return InventoryListSerializer
        if self.action == 'retrieve':
            return InventoryRetrieveSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(
            organization_id=self.request.user.org_id
        ).select_related('group__parent', 'type', 'contract', 'measure_unit')

    @action(detail=False, methods=['GET'], url_path='select')
    def select(self, request):
        queryset = self.queryset.filter(
            organization_id=self.request.user.org_id,
            is_active=True
        ).exclude(stocktakings__terminate_date__isnull=False).annotate(
            value=F('id'),
            label=F('name')
        ).values('value', 'label')
        return Response(queryset)

    # @action(detail=True, methods=['post'], url_path='checking')
    # def checking(self, request, pk):
    #     instance = self.get_object()
    #     instance.checking()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
