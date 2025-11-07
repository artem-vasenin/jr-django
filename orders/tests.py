import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.core.management import call_command
from django.contrib.sessions.middleware import SessionMiddleware

from orders.cert_session import Cart
from products.models import Product


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