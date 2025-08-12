from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank = True, null = True)
    name = models.CharField(max_length=200,null = True)
    email = models.EmailField(max_length=200)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank = True)

    def __str__(self):
        return self.name
# This order is like a cart where the things you ordered are placed
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add= True)
    complete = models.BooleanField(default = False)
    transaction = models.BooleanField(max_length = 100, null=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

