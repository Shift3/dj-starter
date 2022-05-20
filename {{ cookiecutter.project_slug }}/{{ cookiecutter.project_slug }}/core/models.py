from django.db import models


class Address(models.Model):
    address1 = models.CharField(max_length=1023)
    address2 = models.CharField(max_length=1023, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=16)
