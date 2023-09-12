from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer, ShoeCondition, Product, Order, OrderItem, Shipping
import json, uuid
from .utils import guestUserOrder, productDataUtils
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .forms import CustomUserCreationForm


# Create your views here.


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("shoestore")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            print("Username Incorrect")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("shoestore")
        else:
            print("Username or Password incorrect")

    context = {"page": page}
    return render(request, "shoes/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("shoestore")


def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("shoestore")
        else:
            print("Error occurred during Registrations")
    return render(request, "shoes/login_register.html", {"form": form})


def shoestore(request):
    UserData = productDataUtils(request)
    cartItems = UserData["cartItems"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems, "shippingCharge": 0}
    return render(request, "shoes/shoestore.html", context)


def cart(request):
    UserData = productDataUtils(request)
    items = UserData["items"]
    order = UserData["order"]
    cartItems = UserData["cartItems"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shippingCharge": 0,
    }
    return render(request, "shoes/cart.html", context)


def checkout(request):
    UserData = productDataUtils(request)
    items = UserData["items"]
    order = UserData["order"]
    cartItems = UserData["cartItems"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shippingCharge": 0,
    }
    return render(request, "shoes/checkout.html", context)


def updateCart(request):
    data = json.loads(request.body)
    productId = data["productID"]
    action = data["action"]
    print("Action:", action)
    print("Product:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    print("Data:", request.body)
    transaction_id = uuid.uuid4().hex
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print("Guest User ...")
        print("COOKIES:", request.COOKIES)

        name = data["form"]["name"]
        email = data["form"]["email"]

        guestUserData = guestUserOrder(request)
        items = guestUserData["items"]

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer, complete=False, transaction_id=transaction_id
        )

        for item in items:
            product = Product.objects.get(id=item["product"]["id"])
            orderItem = OrderItem.objects.create(
                product=product, order=order, quantity=item["quantity"]
            )

    total_price = data["form"]["total_price"]
    order.transaction_id = transaction_id

    if float(total_price) == float(order.get_cart_total_price):
        order.complete = True
    order.save()

    Shipping.objects.create(
        customer=customer,
        order=order,
        address=data["shipping"]["address"],
        city=data["shipping"]["city"],
        zipcode=data["shipping"]["zipcode"],
    )

    return JsonResponse("payment complete", safe=False)
