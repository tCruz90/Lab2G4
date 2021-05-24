from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
  user = models.OneToOneField(
      User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=200, null=True)

  def __str__(self):
    return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=200, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
       return self.name


class Order(models.Model):
  customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, blank=True, null= True)