from django.db import models

from common.models import Organization, Department
from utils.abstract_models import BaseModel
from utils.services import generate_code


class Position(BaseModel):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=500)
    code = models.PositiveSmallIntegerField(editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='positions')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(Position, 10, self.organization)
        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = _("Position")
        # verbose_name_plural = _("Positions")
        db_table = 'position'
        unique_together = ('organization', 'code')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Employee(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True, related_name='employees')
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)


    class Meta:
        # verbose_name = _("Employee")
        # verbose_name_plural = _("Employees")
        db_table = 'employee'
        ordering = ['-created_at']


    def __str__(self):
        return self.name
