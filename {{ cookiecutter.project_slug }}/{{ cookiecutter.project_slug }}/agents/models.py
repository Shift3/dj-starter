from {{ cookiecutter.project_slug }}.core.models from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Agent(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    address1 = models.CharField(max_length=1023, null=True, blank=True)
    address2 = models.CharField(max_length=1023, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=16, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
        ]
