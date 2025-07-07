import os
from datetime import datetime

from django.core.files.storage.filesystem import FileSystemStorage
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView

from shopapp.models import Product, Order
from .forms import ProductForm


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        prod = [('Mobile', 1000), ('Desktop', 2000), ('Laptop', 3000)]
        ctx = {"date": datetime.now(), "prod": prod}
        return render(request, 'shopapp/index.html', ctx)

class GroupListView(ListView):
    template_name = 'shopapp/group-list.html'
    queryset = Group.objects.prefetch_related('permissions').all()
    context_object_name = 'list'

class OrderListView(ListView):
    # template_name = 'shopapp/order-list.html' # shopapp/order_list.html по умолчанию
    queryset = Order.objects.select_related('user').prefetch_related('products')
    # context_object_name = 'list' # object_list по умолчанию

class ProductListView(ListView):
    template_name = 'shopapp/product-list.html'
    model = Product
    context_object_name = 'list'

class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'

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
