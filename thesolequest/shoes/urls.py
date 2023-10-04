from django.urls import path
from . import views

urlpatterns = [
    path("", views.shoestore, name="shoestore"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("detail/<str:pk>/", views.shoeDetails, name="shoe-detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update-cart/", views.updateCart, name="update-cart"),
    path("process-order/", views.processOrder, name="process-order"),
    path("error-404/", views.errorPage, name="error-page"),
    path("userprofile/<str:pk>/", views.userProfile, name="user-profile"),
]
