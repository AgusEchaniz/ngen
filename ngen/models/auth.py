from django.contrib.auth.models import AbstractUser
from django.db import models

from ngen.models.common.mixins import AuditModelMixin, PriorityModelMixin


class User(AbstractUser, PriorityModelMixin, AuditModelMixin):
    api_key = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        db_table = 'user'
