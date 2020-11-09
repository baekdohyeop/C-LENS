from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    indexes = ArrayField(
        models.CharField(max_length=20)
    )