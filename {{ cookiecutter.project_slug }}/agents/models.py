from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from boilerplate.core.models import Address


class Agent(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]
