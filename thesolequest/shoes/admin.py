from django.contrib import admin
from .models import (
    Customer,
    ShoeCondition,
    Product,
    Order,
    OrderItem,
    Shipping,
    ShoeBrand,
)

# Register your models here.

admin.site.register(Customer)
admin.site.register(ShoeCondition)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipping)
admin.site.register(ShoeBrand)
