from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views import View


class ManagementView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/index.html')

class ManagementProductsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/products.html')

class ManagementProductView(View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        return render(request, 'management/product.html', {pk: pk})

class ManagementAddProductView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/add-product.html')
