from django.db import models

# Create your models here.






class Categoryies(models.Model):
    category_name = models.CharField( max_length=50)
    description = models.CharField(max_length=200)


    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    stock = models.IntegerField()
    category  = models.ForeignKey(Categoryies, on_delete=models.CASCADE, null=True, blank=True)
    image = models.CharField(max_length=2500)
    image2 = models.CharField(max_length=2500, null=True)

    def __str__(self):
        return self.name

