from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.views import View

from .cert_session import Cart
from products.models import Product


class CartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})

    def post(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        product_id = request.POST['product_id']
        next_page = request.POST['next_page']
        product = get_object_or_404(Product, id=product_id)
        if request.POST.get('action') == 'inc':
            cart.change(product)
        if request.POST.get('action') == 'dec':
            cart.change(product, True)
        if request.POST.get('action') == 'del':
            cart.remove(product)
        return redirect(next_page) if next_page else redirect('products:product', product.slug)

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.remove(product)
        return redirect('orders:cart')

class CheckoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'orders/checkout.html')
