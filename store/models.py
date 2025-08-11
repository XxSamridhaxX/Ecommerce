from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank = True, null = True)
    name = models.CharField(max_length=200,null = True)
    email = models.EmailField(max_length=200)
    def __str__(self):
        return self.name