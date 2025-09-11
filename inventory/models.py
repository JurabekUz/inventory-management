import os
from django.urls import reverse
from django.conf import settings
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from common.models import InventoryGroup, InventoryType, MeasureUnit
from contract.models import Contract
from organization.models import Organization
from utils.abstract_models import BaseModel
from utils.services import generate_code


def validate_group(group):
    if group.children.exists():
        raise ValidationError(_("Invalid group, could not select this group"))


def qr_file_upload_to(instance, filename):
    return os.path.join(str(instance.organization.code), 'QR-Codes', filename)


class Inventory(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventories')
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=500)
    code = models.PositiveSmallIntegerField(editable=False)
    group = models.ForeignKey(
        InventoryGroup, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='inventories',
        validators=[validate_group]
    )
    type = models.ForeignKey(
        InventoryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventories')
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventories')
    measure_unit = models.ForeignKey(
        MeasureUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventories')
    amount = models.FloatField()
    price = models.DecimalField(decimal_places=2, max_digits=14)
    total_value = models.DecimalField(decimal_places=2, max_digits=14)
    qqs = models.BooleanField()
    date = models.DateField()
    terminate_date = models.DateField(blank=True, null=True)
    qr_file = models.FileField(upload_to=qr_file_upload_to, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(Inventory, 1, self.organization)
        super().save(*args, **kwargs)

        # Generate and attach the QR code
        if not self.qr_file:
            self.generate_and_attach_qr_code()

    def generate_and_attach_qr_code(self):
        # Create the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Generate the URL for the inventory's retrieve page
        inventory_detail_url = reverse('inventory-detail', args=[self.id])
        full_url = f"{settings.SITE_URL}{inventory_detail_url}"

        # Add the URL to the QR code data
        qr.add_data(full_url)
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Create a filename for the QR code based on the inventory code
        filename = f"{self.code}.png"

        # Save the image to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_content = ContentFile(buffer.getvalue())
        self.qr_file.save(filename, file_content)

    class Meta:
        # verbose_name = _("Inventory")
        # verbose_name_plural = _("Inventories")
        db_table = 'inventory'
        unique_together = ('organization', 'code')
        ordering = ['-created_at']


    def __str__(self):
        return self.name
