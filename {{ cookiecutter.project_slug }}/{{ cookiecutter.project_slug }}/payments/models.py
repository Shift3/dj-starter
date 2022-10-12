from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)

    def _str_(self):
      return self.name