from django.http import HttpRequest
from orders.cert_session import Cart


def orders_context(request: HttpRequest):
    cart = Cart(request)

    return {
        'cart': cart,
        'cart_len': len(cart),
    }