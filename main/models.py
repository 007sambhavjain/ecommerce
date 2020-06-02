from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,related_name='customer',on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50)
    mobile_number=models.CharField(max_length=20)
    money=models.FloatField(default=0)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='vendor',on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50)
    mobile_number=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    vendor=models.ForeignKey('Vendor',related_name='vendor',on_delete=models.CASCADE,blank=True,null=True)
    customer=models.ForeignKey('Customer',related_name='customer',on_delete=models.CASCADE,blank=True,null=True)
    title=models.CharField(max_length=20)
    cost=models.FloatField()
    image=models.ImageField(upload_to= '',null=True,blank=True)
    description=models.CharField(max_length=50,blank=True,null=True)
    quantity=models.FloatField(blank=True,null=True)
    
    def __str__(self):
        return self.title


    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''

        return url   

class Order(models.Model):
    customer=models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True,blank=True) 
    quantity=models.FloatField(default=1,blank=True,null=True)
    vend=models.ForeignKey('Vendor',related_name='vend',on_delete=models.CASCADE,null=True,blank=True) 
    prod=models.ForeignKey('Product',related_name='prod',on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return str(self.id)            


class Orderitem(models.Model):
    product=models.ForeignKey('Product',related_name='product',on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.FloatField(default=1,blank=True,null=True)
    custom=models.ForeignKey('Customer',related_name='custom',on_delete=models.CASCADE,blank=True,null=True)
    ven=models.ForeignKey('Vendor',related_name='ven',on_delete=models.CASCADE,null=True,blank=True) 
    def __str__(self):
        return self.product.title
    @property
    def total(self):
        tot=(self.product.cost)*(self.quantity)
        return tot


         

# class Orderitem(models.Model):  
#     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True) 
#     product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)  
#     quantity=models.IntegerField(default=0,null=True)
  

#     def __str__(self):
#         return self.product.title


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)  
    order=models.ForeignKey(Orderitem,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=100,null=False)
    city=models.CharField(max_length=100,null=False)
    state=models.CharField(max_length=100,null=False)
 
  

    def __str__(self):
         return self.address




