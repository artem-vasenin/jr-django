from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from shopapp.models import Product, Order


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
    queryset = Order.objects.select_related('user').prefetch_related('products')

class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/product-list.html'
    # model = Product
    context_object_name = 'list'
    queryset = Product.objects.filter(archived=False)

class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'discount']
    success_url = reverse_lazy('shopapp:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'discount']

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk}
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
