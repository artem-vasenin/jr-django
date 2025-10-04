from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views import View


class CartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'orders/cart.html')

class CheckoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'orders/checkout.html')
