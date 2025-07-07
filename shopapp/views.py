import os
from datetime import datetime

from django.core.files.storage.filesystem import FileSystemStorage
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View

from shopapp.models import Product, Order
from .forms import ProductForm


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        prod = [('Mobile', 1000), ('Desktop', 2000), ('Laptop', 3000)]
        ctx = {"date": datetime.now(), "prod": prod}
        return render(request, 'shopapp/index.html', ctx)

class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {'list': Group.objects.prefetch_related('permissions').all()}
        return render(request, 'shopapp/group-list.html', ctx)

class OrderListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {'list': Order.objects.select_related('user').prefetch_related('products').all()}
        return render(request, 'shopapp/order-list.html', ctx)

class ProductListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {'list': Product.objects.all()}
        return render(request, 'shopapp/product-list.html', ctx)

class ProductDetailsView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        ctx = {'product': product}
        return render(request, 'shopapp/product-details.html', ctx)

class ProductFormView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm()
        ctx = {'form': form}
        return render(request, 'shopapp/product-form.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = {**form.cleaned_data}
            del data["image"]
            product = Product.objects.create(**data)
            file = request.FILES.get('image')
            fs = FileSystemStorage(location=os.path.join('shopapp', 'files'))
            fs.save(f'{product.pk}_{file.name}', file)

        return redirect(reverse('shopapp:product_list'))
