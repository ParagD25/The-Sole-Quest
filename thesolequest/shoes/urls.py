from django.urls import path
from . import views

urlpatterns = [
    path("", views.shoestore, name="shoestore"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update-cart/", views.updateCart, name="update-cart"),
    path("process-order/", views.processOrder, name="process-order"),
]
