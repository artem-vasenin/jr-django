import time
import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.sessions.middleware import SessionMiddleware

from orders.cert_session import Cart
from products.models import Product
from orders.models import Order, OrderItem, PaymentMethod


def add_session_to_request(request):
    """Подключаем сессию к request"""
    middleware = SessionMiddleware(get_response=lambda r: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture(autouse=True, scope='function')
def load_db_fixtures(db):
    """Подключаем фикстуры к каждому тесту"""
    call_command('loaddata', 'db_fixtures.json')


@pytest.mark.django_db
def test_add_product_to_cart():
    """ Проверка добавления товара в корзину """
    product = Product.objects.get(pk=1)

    factory = RequestFactory()
    request = factory.get('/')
    request = add_session_to_request(request)

    cart = Cart(request)
    cart.change(product, qty=2)

    assert str(product.pk) in cart.cart
    assert cart.cart[str(product.pk)]['qty'] == 2
    assert Decimal(cart.cart[str(product.pk)]['price']) == product.price
    assert cart.get_total_price() == Decimal('3.60')


@pytest.mark.django_db
def test_remove_product_from_cart():
    """ Проверка удаления товара из корзины """
    product1 = Product.objects.get(pk=1)
    product2 = Product.objects.get(pk=2)

    factory = RequestFactory()
    request = factory.get('/')
    request = add_session_to_request(request)

    cart = Cart(request)
    cart.change(product1, qty=2)
    cart.change(product2, qty=1)

    cart.remove(product1)

    assert str(product1.pk) not in cart.cart
    assert str(product2.pk) in cart.cart
    assert cart.cart[str(product2.pk)]['qty'] == 1
    assert Decimal(cart.cart[str(product2.pk)]['price']) == product2.price
    assert cart.get_total_price() == Decimal('7.49')


@pytest.mark.django_db
def test_order_from_cart():
    """ Проверка создания заказа из корзины """
    user = User.objects.get(pk=1)
    profile = getattr(user, 'profile', None)
    product = Product.objects.get(pk=1)
    method = PaymentMethod.objects.get(pk=1)

    profile.balance = 50
    profile.save(update_fields=['balance'])

    factory = RequestFactory()
    request = factory.get('/')
    request = add_session_to_request(request)

    cart = Cart(request)
    cart.change(product, qty=2)

    order = Order.objects.create(
        order_id=f'{user.pk}_{int(time.time())}',
        status='pending',
        user=user,
        city='Tver',
        phone='79888888888',
        address='Mira',
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

    total = Decimal(order.total_price or 0)
    if profile.balance >= total > 0:
        profile.balance -= total
        profile.save(update_fields=['balance'])
        order.status = Order.Status.PAID
        order.save(update_fields=['status'])

    cart.remove(product)

    assert len(cart) == 0
    assert Order.objects.count() == 1
    assert order.items.count() == 1
    assert order.total_price == Decimal('3.60')
