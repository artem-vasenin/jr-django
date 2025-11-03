import time
from decimal import Decimal
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm
from .cert_session import Cart
from products.models import Product
from .models import PaymentMethod, Order, OrderItem
from accounts.mixins import AuthenticatedRequiredMixin


class CartView(View):
    """ Контроллер корзины товаров """
    def get(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})

    def post(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        next_page = request.POST.get('next_page')
        product = get_object_or_404(Product, id=product_id)
        if request.POST.get('action') == 'inc':
            if product.stock >= cart.in_cart(product) + 1:
                cart.change(product)
        if request.POST.get('action') == 'dec':
            cart.change(product, True)
        if request.POST.get('action') == 'del':
            cart.remove(product)

        return redirect(next_page) if next_page else redirect('products:product', product.slug)

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.remove(product)

        return redirect('orders:cart')


class CheckoutView(AuthenticatedRequiredMixin, View):
    """ Контроллер создания заказа из корзины """
    template_name = 'orders/checkout.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        first_method = PaymentMethod.objects.first()
        form = OrderForm(initial={
            'phone': request.user.profile.phone,
            'city': request.user.profile.city,
            'address': request.user.profile.address,
            'method': first_method.pk if first_method else None
        })
        ctx = {'form': form, 'cart': cart}

        return render(request, self.template_name, ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        form = OrderForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    phone = form.cleaned_data.get('phone')
                    city = form.cleaned_data.get('city')
                    address = form.cleaned_data.get('address')
                    method = form.cleaned_data.get('method')

                    order = Order.objects.create(
                        order_id = f'{request.user.pk}_{int(time.time())}',
                        status='pending',
                        user=request.user,
                        city=city,
                        phone=phone,
                        address=address,
                        method=method,
                    )

                    for p in cart.items():
                        product = Product.objects.filter(pk=p['product'].pk).first()
                        if product:
                            OrderItem.objects.create(
                                order_id=order.pk,
                                product=product,
                                quantity=p['qty'],
                                price=p['price'],
                            )
                            product.stock -= p['qty']
                            product.save(update_fields=['stock'])

                    profile = getattr(request.user, 'profile', None)
                    if profile:
                        total = Decimal(order.total_price or 0)
                        if profile.balance >= total > 0:
                            profile.balance -= total
                            profile.save(update_fields=['balance'])
                            order.status = Order.Status.PAID
                            order.save(update_fields=['status'])

                    cart.clear()
                    messages.success(request, f'Order {order.order_id} created')
                    return redirect('home')

            except Exception as e:
                print('Error', e)
                messages.error(request, 'Order is not create')

        ctx = {'form': form, 'cart': cart}
        return render(request, self.template_name, ctx)
