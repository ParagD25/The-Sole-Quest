from django.shortcuts import render
from django.http import JsonResponse
from .models import Customer, ShoeCondition, Product, Order, OrderItem, Shipping
import json, uuid

# Create your views here.


def shoestore(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_total_items
    else:
        items = []
        order = {"get_cart_total_items": 0, "get_cart_total_price": 0}
        cartItems = order["get_cart_total_items"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems, "shippingCharge": 0}
    return render(request, "shoes/shoestore.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_total_items
    else:
        items = []
        order = {"get_cart_total_items": 0, "get_cart_total_price": 0}
        cartItems = order["get_cart_total_items"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shippingCharge": 0,
    }
    return render(request, "shoes/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_total_items
    else:
        items = []
        order = {"get_cart_total_items": 0, "get_cart_total_price": 0}
        cartItems = order["get_cart_total_items"]

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

    else:
        print("User not checked out")
    return JsonResponse("payment complete", safe=False)
