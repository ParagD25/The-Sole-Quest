from django.urls import path
from . import views

urlpatterns = [
    path("", views.shoestore, name="shoestore"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
]
