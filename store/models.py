from django.db import models
from django.contrib.auth.models import User
import os

from PIL import Image,ImageFilter
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
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name
    
    # def save(self,*args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.image and hasattr(self.image, 'path'):
    #         img = Image.open(self.image.path)

    #         if img.width > 640 or img.width >360:
    #             img.thumbnail((600,320))
    #             img = img.filter(ImageFilter.SHARPEN)
    #             save_path = os.path.join(os.path.dirname(self.image.path), "gayshit.jpg")
    #             img.save(save_path)

    #             self.image.name = os.path.join(os.path.dirname(self.image.name),'gayshit.jpg')
    #             super().save(update_fields = ['image'])
""" Note: save is a method to save item in db we're overriding the save function of the superclass
    Thumbnail resizes the picture without stretching or distorting
    img.save means saving into same path where the image is resized
 """
    

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


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)    
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
