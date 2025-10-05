from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .forms import CategoryForm
from products.models import Category
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
        categories_list = Category.objects.all().order_by('id')
        paginator = Paginator(categories_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(page_obj.has_previous())
        print(page_obj.has_next())
        return render(request, 'management/categories.html', {'page_obj': page_obj})


class ManagementCategoryView(SuperuserRequiredMixin, View):
    template_name = 'management/category.html'

    def get(self, request: HttpRequest, pk) -> HttpResponse:
        category = Category.objects.filter(id=pk).first()
        initial = {'name': category.name, 'parent': category.parent}
        form = CategoryForm(initial=initial)
        return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request: HttpRequest, pk) -> HttpResponse:
        category = Category.objects.filter(id=pk).first()
        if not category:
            messages.error(request, 'Category does not found')
            return render(request, self.template_name, {'form': CategoryForm(request.POST)})

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')

            return redirect('management-categories')
        return render(request, self.template_name, {'form': form})


class ManagementAddCategoryView(SuperuserRequiredMixin, View):
    template_name = 'management/add-category.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')

            return redirect('management-categories')
        return render(request, self.template_name, {'form': form})


class ManagementDeleteCategoryView(SuperuserRequiredMixin, View):
    def post(self, request: HttpRequest, pk:int) -> HttpResponse:
        category = Category.objects.filter(pk=pk).first()
        if category:
            category.delete()
            messages.success(request, 'Category deleted successfully')

        return redirect('management-categories')
