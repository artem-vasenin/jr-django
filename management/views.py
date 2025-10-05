from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from accounts.mixins import SuperuserRequiredMixin


class ManagementView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/index.html')

class ManagementProductsView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/products.html')

class ManagementProductView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        return render(request, 'management/product.html', {pk: pk})

class ManagementAddProductView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/add-product.html')

class ManagementCategoriesView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/categories.html')

class ManagementCategoryView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        return render(request, 'management/category.html', {pk: pk})

class ManagementAddCategoryView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/add-category.html')
