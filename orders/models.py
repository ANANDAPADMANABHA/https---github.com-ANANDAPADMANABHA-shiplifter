from django.db import models
from accounts.models import Account, Address
from cartapp.models import Cart, CartItem
from theproducts.models import Product

# Create your models here.


class Orders(models.Model):

    STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out_for_delivery','Out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )

    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    address     =   models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
    ordertotal  =   models.FloatField(max_length=50 ,null=True)
    orderid     =   models.CharField(max_length=20,null=True)
    date        =   models.DateField(null=True)
    status      =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')

class OrderProduct(models.Model):
    
    order       =   models.ForeignKey(Orders,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    quantity    =   models.IntegerField(null=True)
    price       =   models.FloatField(max_length=200,null=True)

    def sub_total(self):
        return self.price * self.quantity