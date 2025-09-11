from django.contrib.auth.models import AbstractUser
from django.db import models

from organization.models import Organization


class User(AbstractUser):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

