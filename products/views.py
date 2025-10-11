from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest

from .models import Product


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = Product.objects.all().order_by('-created_at')
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'products/index.html', {
            'page_obj': page_obj,
            'paginator': paginator,
        })

class GuidesView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'products/guides.html')

class DetailsView(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        object = get_object_or_404(Product, slug=slug)
        return render(request, 'products/details.html', {'object': object})
