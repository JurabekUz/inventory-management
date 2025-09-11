from django.db import models

from common.models import Attachment
from organization.models import Organization
from utils.abstract_models import BaseModel
from utils.attachment import get_attachments_by_object


class Contract(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='contracts')
    number = models.CharField(max_length=10)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # verbose_name = _("Contract")
        # verbose_name_plural = _("Contracts")
        db_table = 'contract'
        ordering = ['-created_at']
        unique_together = ('organization', 'number')

    def __str__(self):
        return self.number

    def attachment_file(self, *args, **kwargs):
        attachment = get_attachments_by_object(self).first()
        if attachment:
            return attachment.file
        return None


"""
    Shartnomaga tur qo'shsak bo'ladi, kelishuvmi yoki narsa sotib olishmi va hk.
"""