import os

from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .forms import CategoryForm, ProductForm
from products.models import Category, Product
from accounts.mixins import SuperuserRequiredMixin


class ManagementView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'management/index.html')


class ManagementProductsView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        lst = Product.objects.all().order_by('-id')
        paginator = Paginator(lst, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'management/products.html', {'page_obj': page_obj})


class ManagementProductView(SuperuserRequiredMixin, View):
    template_name = 'management/product.html'

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        obj = Product.objects.filter(slug=slug).first()
        if not obj:
            messages.error(request, 'Product does not found')
            return redirect('management:management-products')

        initial = {
            'name': obj.name,
            'description': obj.description,
            'price': obj.price,
            'category': obj.category,
            'stock': obj.stock,
            'is_active': obj.is_active,
            'image': obj.image,
        }
        form = ProductForm(initial=initial)
        return render(request, self.template_name, {'form': form, 'object': obj})

    def post(self, request: HttpRequest, slug: str):
        obj = Product.objects.filter(slug=slug).first()

        if obj:
            if request.POST.get('action') == 'save':
                form = ProductForm(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Product was changed')
                    return redirect('management:management-products')
            elif request.POST.get('action') == 'hide':
                obj.is_active = False
                obj.save()
                messages.success(request, 'Product was hidden')
                return redirect('management:management-products')
            elif request.POST.get('action') == 'delete':
                obj.delete()
                messages.success(request, 'Product deleted successfully')
                return redirect('management:management-products')
        return redirect('management:management-products')


class ManagementAddProductView(SuperuserRequiredMixin, View):
    template_name = 'management/add-product.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')

            return redirect('management:management-products')

        return render(request, self.template_name, {'form': form})


class ManagementCategoriesView(SuperuserRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        categories_list = Category.objects.all().order_by('id')
        paginator = Paginator(categories_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'management/categories.html', {'page_obj': page_obj})


class ManagementCategoryView(SuperuserRequiredMixin, View):
    template_name = 'management/category.html'

    def get(self, request: HttpRequest, slug) -> HttpResponse:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            messages.error(request, 'Category does not found')
            return redirect('management:management-categories')

        initial = {'name': category.name, 'parent': category.parent}
        form = CategoryForm(initial=initial)
        return render(request, self.template_name, {'form': form, 'pk': category.pk})

    def post(self, request: HttpRequest, slug) -> HttpResponse:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            messages.error(request, 'Category does not found')
            return render(request, self.template_name, {'form': CategoryForm(request.POST)})

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')

            return redirect('management:management-categories')
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

            return redirect('management:management-categories')
        return render(request, self.template_name, {'form': form})


class ManagementDeleteCategoryView(SuperuserRequiredMixin, View):
    def post(self, request: HttpRequest, pk:int) -> HttpResponse:
        category = Category.objects.filter(pk=pk).first()
        if category:
            category.delete()
            messages.success(request, 'Category deleted successfully')

        return redirect('management:management-categories')
