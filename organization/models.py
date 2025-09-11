from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstract_models import BaseModel


class OrgTypes(models.IntegerChoices):
    physical = 1, _("Physical")
    legal = 2, _("Legal")
    others = 3, _("Others")


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=500)
    code = models.PositiveSmallIntegerField(unique=True, editable=False)
    type = models.IntegerField(choices=OrgTypes.choices, default=OrgTypes.legal)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    inn = models.CharField(max_length=9, blank=True, null=True)
    register_date = models.DateField(blank=True, null=True)
    register_number = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Organization.objects.aggregate(models.Max('code', default=0))['code__max'] + 1
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Organization")
        # verbose_name_plural = _("Organizations")
        db_table = 'organization'
        ordering = ['-created_at']



    def __str__(self):
        return self.name
