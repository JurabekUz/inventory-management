import os
import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from organization.models import Organization
from utils.abstract_models import BaseModel
from utils.services import generate_code


class Department(BaseModel):
    name = models.CharField(max_length=255)
    code = models.PositiveSmallIntegerField(editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(Department, 1, self.organization)
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Department")
        # verbose_name_plural = _("Departments")
        db_table = 'department'
        unique_together = ('organization', 'code')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class InventoryGroup(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    name = models.CharField(max_length=255)
    code = models.PositiveSmallIntegerField(editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='groups')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(InventoryGroup, 1, self.organization)
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Inventory Group")
        # verbose_name_plural = _("Inventory Groups")
        db_table = 'inventory_group'
        unique_together = ('organization', 'code')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class InventoryType(BaseModel):
    name = models.CharField(max_length=255)
    code = models.PositiveSmallIntegerField(editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventory_types')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(InventoryType, 1, self.organization)
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Inventory Type")
        # verbose_name_plural = _("Inventory Types")
        db_table = 'inventory_type'
        unique_together = ('organization', 'code')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class NumberTypes(models.IntegerChoices):
    integer = 1, _("Integer")
    optional = 2, _("Optional")


class MeasureUnit(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='measure_units')
    number_type = models.IntegerField(choices=NumberTypes.choices, default=NumberTypes.integer)

    class Meta:
        # verbose_name = _("Measure Unit")
        # verbose_name_plural = _("Measure Units")
        db_table = 'measure_unit'
        unique_together = ('organization', 'name')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


def attachment_upload_to(instance, filename):
    # Get the model name of the related content object
    model_name = instance.content_object._meta.model_name

    # Check if the content_object has a related user and organization
    organization = getattr(instance.content_object, 'organization', None)
    if organization:
        org_code = organization.code
    else:
        org_code = 'unknown'

    # Generate the folder path based on the model name and user's organization code
    return os.path.join(str(org_code), model_name, filename)


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(upload_to=attachment_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.content_object}"
