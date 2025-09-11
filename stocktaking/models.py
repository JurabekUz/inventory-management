import uuid

from django.db import models

from employee.models import Employee
from inventory.models import Inventory
from users.models import User
from utils.abstract_models import BaseModel


class Stocktaking(BaseModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='stocktakings')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='stocktakings')
    number = models.PositiveBigIntegerField(auto_created=True)
    date = models.DateField()
    terminate_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = Stocktaking.objects.filter(
                inventory__organization=self.inventory.organization
            ).aggregate(models.Max('number', default=0))['number__max'] + 1
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Stocktaking")
        # verbose_name_plural = _("Stocktakings")
        db_table = 'stocktaking'
        ordering = ['-created_at']


    def __str__(self):
        return str(self.number)


class Inspection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stocktaking = models.ForeignKey(Stocktaking, on_delete=models.CASCADE, related_name='inspections')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inspection'
        unique_together = ('stocktaking', 'created_at')
        ordering = ['-created_at']

