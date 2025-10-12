from django.views import View
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest

from .models import Product, Category
from .forms import ReviewForm


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        categories = Category.objects.all()
        products = Product.objects.filter(is_active=True).order_by('-created_at')

        q = request.GET.get('q')
        sort = request.GET.get('sort')
        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

        if sort == 'a_price':
            products = products.order_by('price')
        elif sort == 'd_price':
            products = products.order_by('-price')
        elif sort == 'rating':
            products = products.order_by('-rating')
        else:
            products = products.order_by('-created_at')

        selected_categories = request.GET.getlist('category')
        if selected_categories:
            products = products.filter(category__id__in=selected_categories)

        querydict = request.GET.copy()
        if 'page' in querydict:
            querydict.pop('page')
        querystring = querydict.urlencode()

        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'products/index.html', {
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': categories,
            'querystring': querystring,
            'sort': sort,
            'q': q,
            'selected_categories': list(map(int, selected_categories)),
        })


class GuidesView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'products/guides.html')


class DetailsView(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        object = get_object_or_404(Product, slug=slug)
        review_form = ReviewForm()
        rating_choices = review_form.fields['rating'].choices
        ctx = {
            'object': object,
            'review_form': review_form,
            'rating_choices': rating_choices,
        }
        return render(request, 'products/details.html', ctx)


class AddReviewView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        print(request.POST)
        return HttpResponse(request)
