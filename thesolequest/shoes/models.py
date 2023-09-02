from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name


class ShoeCondition(models.Model):
    condition = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.condition


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    condition = models.ForeignKey(
        ShoeCondition, on_delete=models.SET_NULL, blank=True, null=True
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{str(self.id)} - {str(self.transaction_id)}"

    @property
    def get_cart_total_price(self):
        orderitems = self.orderitem_set.all()
        total_price = sum([item.get_total for item in orderitems])
        return total_price + self.shippingCharge

    @property
    def get_cart_total_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum([item.quantity for item in orderitems])
        return total_items

    @property
    def shippingCharge(self):
        orderitems = self.orderitem_set.all()
        total_items = sum([item.quantity for item in orderitems])
        total_cost = sum([item.get_total for item in orderitems])
        if total_cost > 24999:
            shippingCharge = 0
        else:
            shippingCharge = 1250
        return shippingCharge


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.id)} - {str(self.product.name)}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Shipping(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
