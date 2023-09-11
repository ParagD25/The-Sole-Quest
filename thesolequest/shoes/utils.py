import json
from .models import *


def guestUserOrder(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    items = []
    order = {"get_cart_total_items": 0, "get_cart_total_price": 0}
    cartItems = order["get_cart_total_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order["get_cart_total_price"] += total
            order["get_cart_total_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }
            items.append(item)
        except:
            pass

    return {"cartItems": cartItems, "order": order, "items": items}


def productDataUtils(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_total_items
    else:
        guestUser = guestUserOrder(request)
        items = guestUser["items"]
        order = guestUser["order"]
        cartItems = guestUser["cartItems"]
    return {"cartItems": cartItems, "order": order, "items": items}
