import logging
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count, Q, Value, FloatField

from .forms import ReviewForm
from orders.models import Order
from orders.cert_session import Cart
from .models import Product, Category
from accounts.mixins import AuthenticatedRequiredMixin


logger = logging.getLogger('logs')


class HomeView(View):
    """ Контроллер домашней страницы-каталога """
    def get(self, request: HttpRequest) -> HttpResponse:
        categories = Category.objects.all()
        products = (Product.objects
                    .filter(is_active=True)
                    .select_related('category')
                    .prefetch_related('reviews')
                    .order_by('-created_at')
        )

        q = request.GET.get('q') or ''
        sort = request.GET.get('sort')
        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

        if sort == 'a_price':
            products = products.order_by('price')
        elif sort == 'd_price':
            products = products.order_by('-price')
        elif sort == 'rating':
            products = (
                products
                .annotate(
                    avg_rating=Coalesce(Avg('reviews__rating'), Value(-1), output_field=FloatField()),
                    has_rating=Count('reviews', filter=Q(reviews__rating__isnull=False)),
                )
                .order_by('-has_rating', '-avg_rating')
            )
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
    """ Контроллер заглушки (не знаю зачем она) """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'products/guides.html')


class DetailsView(View):
    """ Контроллер детальной инфо товара """
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        user = request.user
        obj = get_object_or_404(Product, slug=slug)
        is_bought = Order.objects.filter(
            user=user,
            status=Order.Status.PAID,
            items__product_id=obj.pk,
        ).exists() if user.is_authenticated else False
        cart = Cart(request)
        review_form = ReviewForm()
        rating_choices = review_form.fields['rating'].choices
        reviews = obj.reviews.order_by('-id')[:3]
        cant_review = False

        if (
            not user.is_authenticated
            or (user.is_authenticated and obj.reviews.filter(user=user).exists())
            or (user.is_authenticated and not is_bought)
        ):
            cant_review = True

        ctx = {
            'object': obj,
            'review_form': review_form,
            'rating_choices': rating_choices,
            'reviews': reviews,
            'cant_review': cant_review,
            'in_cart': cart.in_cart(obj),
        }

        return render(request, 'products/details.html', ctx)


class AddReviewView(AuthenticatedRequiredMixin, View):
    """ Контроллер добавления оценки и коммента к товару """
    def post(self, request: HttpRequest) -> HttpResponse:
        next_url = request.GET.get('next') or '/'
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно добавлен')
            logger.info('Товары: Отзыв успешно добавлен')
        else:
            messages.error(request, 'Отзыв не добавлен')
            logger.info('Товары: Отзыв не добавлен')

        return redirect(next_url)
