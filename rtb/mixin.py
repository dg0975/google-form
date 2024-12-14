from django.db import models

from rtb.managers import ModelManager
from model_utils.models import TimeStampedModel


class StatusMixin(TimeStampedModel):
    is_active = models.BooleanField("active", default=True)
    is_deleted = models.BooleanField("deleted", default=False)


    objects = ModelManager()

    class Meta:
        abstract = True