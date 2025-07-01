from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from datetime import datetime

from django.shortcuts import render

from shopapp.models import Product


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
