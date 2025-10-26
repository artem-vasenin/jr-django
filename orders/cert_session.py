from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest

from products.models import Product


class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def change(self, product: Product, dec=False, qty=1):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': qty, 'price': str(product.price)}
        else:
            if dec:
                if self.cart[product_id]['qty'] == 1:
                    self.remove(product)
                else:
                    self.cart[product_id]['qty'] -= 1
            else:
                self.cart[product_id]['qty'] += qty

    def save(self):
        self.session.modified = True

    def remove(self, product: Product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def in_cart(self, product: Product) -> int:
        product_id = str(product.pk)
        if product_id in self.cart:
            return self.cart[product_id]['qty']
        return 0

    def __str__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for p in products:
            item = cart[str(p.pk)]
            item['product'] = p
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['qty'] for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
