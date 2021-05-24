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
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
       return self.name
     
    @property
    def imageURL(self):
      try:
        url = self.image.url
      except:
        url =''
      return url     


class Order(models.Model):
  customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
  date_order = models.DateTimeField(auto_now_add=True)
  digital = models.BooleanField(default=False, null=True, blank=False)
  complete = models.BooleanField(default=False, null=True, blank=False)
  transaction_id = models.CharField(max_length=100, null=True)


  def __str__(self):
      return str(self.id)
    
  
  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
  
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = ([item.quantity for item in orderitems])
    return total
  
  
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
      total = self.product.price * self.quantity
      return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
       return self.address
