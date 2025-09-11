from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.exceptions import CommonException
from .models import Stocktaking, Inspection
from .serializers import (StocktakingListSerializer, StocktakingRetrieveSerializer, StocktakingSerializer)
from utils.filters import StocktakingFilter
from utils.mixens import ArchiveMixin, AutoOrgSetMixin


class StocktakingViewSet(ArchiveMixin, ModelViewSet):
    queryset = Stocktaking.objects.filter(is_active=True)
    serializer_class = StocktakingSerializer
    search_fields = ('number',)
    filterset_class = StocktakingFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return StocktakingListSerializer
        if self.action == 'retrieve':
            return StocktakingRetrieveSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(
            inventory__organization_id=self.request.user.org_id
        ).select_related('employee', 'inventory',)

    @action(detail=True, methods=['post'], url_path='checking')
    def checking(self, request, pk):
        instance = self.get_object()
        if Inspection.objects.filter(stocktaking=instance, created_at__date=timezone.now().date()).exists():
            raise CommonException('Inspection is already created in today')
        Inspection.objects.create(stocktaking=instance, user=self.request.user)
        return Response()
