from django.core.files.storage.filesystem import FileSystemStorage
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from datetime import datetime
import os

from django.shortcuts import render, redirect, reverse

from shopapp.models import Product, Order
from .forms import ProductForm


def shop_index(request: HttpRequest) -> HttpResponse:
    prod = [('Mobile', 1000), ('Desktop', 2000), ('Laptop', 3000)]
    ctx = {"date": datetime.now(), "prod": prod}
    return render(request, 'shopapp/index.html', ctx)

def group_list(request: HttpRequest) -> HttpResponse:
    ctx = {'list': Group.objects.prefetch_related('permissions').all()}
    return render(request, 'shopapp/group-list.html', ctx)

def product_list(request: HttpRequest) -> HttpResponse:
    ctx = {'list': Product.objects.all()}
    return render(request, 'shopapp/product-list.html', ctx)

def order_list(request: HttpRequest) -> HttpResponse:
    ctx = {'list': Order.objects.select_related('user').prefetch_related('products').all()}
    return render(request, 'shopapp/order-list.html', ctx)

def product_form(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = {**form.cleaned_data}
            del data["image"]
            product = Product.objects.create(**data)
            file = request.FILES.get('image')
            fs = FileSystemStorage(location=os.path.join('shopapp', 'files'))
            fs.save(f'{product.pk}_{file.name}', file)

            return redirect(reverse('shopapp:product_list'))
    else:
        form = ProductForm()

    ctx = {'form': form}
    return render(request, 'shopapp/product-form.html', ctx)
