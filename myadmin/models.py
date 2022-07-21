from unicodedata import name
from django.db import models

# Create your models here.
class Mydata(models.Model):
    name = models.CharField(max_length=5)
    age = models.CharField(max_length=5)