from django.db.models import F
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.attachment import attach_file_to_object
from utils.exceptions import CommonException
from utils.mixens import ArchiveMixin, OrgFilterMixin
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = Contract
        fields = ['id', 'number', 'date', 'description', 'supplier', 'created_at', 'file']
        extra_kwargs = {
            'organization': {'write_only': True}
        }

    def validate_number(self, value):
        if self.instance:
            raise serializers.ValidationError("Contract number can't be changed")
        elif Contract.objects.filter(number=value, organization_id=self.context['request'].user.org_id).exists():
            raise serializers.ValidationError("Contract number already exists")
        return value

    def get_file(self, obj):
        return obj.attachment_file()


class ContractViewSet(ArchiveMixin, OrgFilterMixin, ModelViewSet):
    queryset = Contract.objects.filter(is_active=True)
    serializer_class = ContractSerializer
    search_fields = ('number', 'supplier', 'description')

    def perform_create(self, serializer):
        serializer.validated_data['organization_id'] = self.request.user.org_id
        instance = serializer.save()
        uploaded_file = self.request.FILES.get('file', None)
        if uploaded_file:
            raise CommonException("Contract file can't be attached")
            # attach_file_to_object(instance, uploaded_file)


    @action(detail=False, methods=['GET'], url_path='select')
    def select(self, request):
        queryset = self.get_queryset().annotate(
            value=F('id'),
            label=F('number')
        ).values('value', 'label')
        return Response(queryset)
