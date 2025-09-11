from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.paginations import CommonPagination
from . import models
from . import serializers
from utils.mixens import ArchiveMixin, AutoOrgSetMixin, SelectMixin


class DepartmentViewSet(ArchiveMixin, AutoOrgSetMixin, SelectMixin, ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    search_fields = ('name', 'code')
    # pagination_class = CommonPagination
    # filterset_fields = ( )

    def get_queryset(self):
        return models.Department.objects.filter(organization_id=self.request.user.org_id, is_active=True)


class InventoryGroupViewSet(ArchiveMixin, AutoOrgSetMixin, ModelViewSet):
    queryset = models.InventoryGroup.objects.all()
    serializer_class = serializers.InventoryGroupSerializer
    search_fields = ('name', 'code')
    filterset_fields = ('parent', )

    def get_queryset(self):
        return models.InventoryGroup.objects.filter(organization_id=self.request.user.org_id, is_active=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.InventoryGroupDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=['GET'], url_path='select')
    def select(self, request):
        exclude = request.query_params.get('exclude', None)
        no_child = request.query_params.get('no_child', None)
        queryset = self.get_queryset().annotate(
            value=F('id'),
            label=F('name')
        ).values('value', 'label')
        if exclude:
            queryset = queryset.exclude(id=exclude)
        if no_child == 'true':
            queryset = queryset.exclude(children__isnull=False)
        return Response(queryset)


class InventoryTypeViewSet(ArchiveMixin, AutoOrgSetMixin, SelectMixin, ModelViewSet):
    queryset = models.InventoryType.objects.all()
    serializer_class = serializers.InventoryTypeSerializer
    search_fields = ('name', 'code')
    # filterset_fields = ( )

    def get_queryset(self):
        return models.InventoryType.objects.filter(organization_id=self.request.user.org_id, is_active=True)


class MeasureUnitViewSet(ArchiveMixin, AutoOrgSetMixin, SelectMixin, ModelViewSet):
    queryset = models.MeasureUnit.objects.all()
    serializer_class = serializers.MeasureUnitSerializer
    search_fields = ('name',)
    filterset_fields = ('number_type', )

    def get_queryset(self):
        return models.MeasureUnit.objects.filter(organization_id=self.request.user.org_id, is_active=True)









