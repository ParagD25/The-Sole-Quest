from django.shortcuts import render

# Create your views here.


def shoestore(request):
    context = {}
    return render(request, "shoes/shoestore.html", context)


def cart(request):
    context = {}
    return render(request, "shoes/cart.html", context)


def checkout(request):
    context = {}
    return render(request, "shoes/checkout.html", context)
