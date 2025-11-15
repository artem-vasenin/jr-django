import logging
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from orders.models import Order
from .forms import CategoryForm, ProductForm
from products.models import Category, Product, Review
from accounts.mixins import SuperuserRequiredMixin


logger = logging.getLogger('logs')


class ManagementView(SuperuserRequiredMixin, View):
    """ Контроллер дашборда кастомной админки """
    def get(self, request: HttpRequest) -> HttpResponse:
        total_sales = (
                Order.objects.filter(status=Order.Status.PAID).annotate(
                    order_total=Sum(
                        ExpressionWrapper(
                            F('items__quantity') * F('items__price'), output_field=DecimalField()
                        )
                    )
                )
                .aggregate(total_sales=Sum('order_total'))
                .get('total_sales') or 0
        )
        total_orders = Order.objects.all().count()
        total_users = User.objects.all().count()
        pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
        ctx = {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_users': total_users,
            'pending_orders': pending_orders,
        }
        return render(request, 'management/index.html', ctx)


class ManagementProductsView(SuperuserRequiredMixin, View):
    """ Контроллер списка товаров каст.адм """
    def get(self, request: HttpRequest) -> HttpResponse:
        lst = Product.objects.all().order_by('-id')
        paginator = Paginator(lst, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'management/products.html', {'page_obj': page_obj})


class ManagementProductView(SuperuserRequiredMixin, View):
    """ Контроллер формы изменения товара каст.адм """
    template_name = 'management/product.html'

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        obj = Product.objects.filter(slug=slug).first()

        if not obj:
            messages.error(request, 'Товар не найден')
            logger.error(f'Менеджмент: Товар не найден')
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

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        obj = Product.objects.filter(slug=slug).first()

        if obj:
            if request.POST.get('action') == 'save':
                form = ProductForm(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    form.save()
                    logger.info('Менеджмент: Товар был обновлен')
                    messages.success(request, 'Товар был обновлен')

                    return redirect('management:management-products')
            elif request.POST.get('action') == 'hide':
                obj.is_active = False
                obj.save(update_fields=['is_active'])
                messages.success(request, 'Товар был скрыт')
                logger.info(f'Менеджмент: Товар ({obj.name}) был скрыт')

                return redirect('management:management-products')
            elif request.POST.get('action') == 'delete':
                obj.delete()
                logger.info(f'Менеджмент: Товар ({obj.name}) был удален')
                messages.success(request, 'Товар был удален')

                return redirect('management:management-products')

        return redirect('management:management-products')


class ManagementAddProductView(SuperuserRequiredMixin, View):
    """ Контроллер формы добавления товара каст.адм """
    template_name = 'management/add-product.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Товар создан')
            logger.info(f'Менеджмент: Товар ({form.name}) создан')

            return redirect('management:management-products')

        return render(request, self.template_name, {'form': form})


class ManagementCategoriesView(SuperuserRequiredMixin, View):
    """ Контроллер списка категорий каст.адм """
    def get(self, request: HttpRequest) -> HttpResponse:
        categories_list = Category.objects.all().order_by('id')
        paginator = Paginator(categories_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'management/categories.html', {'page_obj': page_obj})


class ManagementCategoryView(SuperuserRequiredMixin, View):
    """ Контроллер формы изменения категории каст.адм """
    template_name = 'management/category.html'

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            messages.error(request, 'Категория не найдена')
            logger.error(f'Менеджмент: Категория не найдена')

            return redirect('management:management-categories')

        initial = {'name': category.name, 'parent': category.parent}
        form = CategoryForm(initial=initial)
        return render(request, self.template_name, {'form': form, 'pk': category.pk})

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            messages.error(request, 'Категория не найдена')
            logger.error(f'Менеджмент: Категория не найдена')

            return render(request, self.template_name, {'form': CategoryForm(request.POST)})

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория изменена')
            logger.info(f'Менеджмент: Категория ({form.name}) изменена')

            return redirect('management:management-categories')

        return render(request, self.template_name, {'form': form})


class ManagementAddCategoryView(SuperuserRequiredMixin, View):
    """ Контроллер формы добавления категории каст.адм """
    template_name = 'management/add-category.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория добавлена')
            logger.info(f'Менеджмент: Категория ({form.name}) добавлена')

            return redirect('management:management-categories')

        return render(request, self.template_name, {'form': form})


class ManagementDeleteCategoryView(SuperuserRequiredMixin, View):
    """ Контроллер формы удаления категории каст.адм """
    def post(self, request: HttpRequest, pk:int) -> HttpResponse:
        category = Category.objects.filter(pk=pk).first()
        name = category.name
        if category:
            category.delete()
            messages.success(request, 'Category deleted successfully')
            logger.info(f'Менеджмент: Категория ({name}) удалена')

        return redirect('management:management-categories')


class ManagementUsersView(SuperuserRequiredMixin, View):
    """ Контроллер списка пользователей каст.адм """
    template_name = 'management/users.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        lst = User.objects.all().order_by('id')
        paginator = Paginator(lst, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj})

    def post(self, request: HttpRequest) -> HttpResponse:
        user_id = request.POST.get('id')

        if user_id:
            user = User.objects.filter(pk=user_id).first()
            if user:
                user.is_active = not user.is_active
                user.save(update_fields=['is_active'])
                logger.info(f'Менеджмент: Активность пользователя ({user.get_username()}) изменена')

        return redirect('management:management-users')


class ManagementReviewsView(SuperuserRequiredMixin, View):
    """ Контроллер списка отзывов каст.адм """
    template_name = 'management/reviews.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        lst = Review.objects.all().order_by('id')
        paginator = Paginator(lst, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj})

    def post(self, request: HttpRequest) -> HttpResponse:
        review_id = request.POST.get('id')

        if review_id:
            review = Review.objects.filter(pk=review_id).first()
            if review:
                review.is_active = not review.is_active
                review.save(update_fields=['is_active'])
                logger.info(f'Менеджмент: Видимость отзыва изменена')

        return redirect('management:management-reviews')
