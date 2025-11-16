# orders/test_graphql.py
import json
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.sessions.middleware import SessionMiddleware

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


@pytest.fixture
def user(db):
    """Подключаем обычного пользователя"""
    user = User.objects.create_user(username="testuser", password="12345")
    user.profile.balance = 1000
    user.profile.save(update_fields=['balance'])
    return user


@pytest.fixture
def token(client, user):
    """Отдает токен обычного пользователя"""
    mutation = f"""
        mutation {{
          tokenAuth(username: "{user.username}", password: "12345") {{
            token
          }}
        }}
        """
    token_response = client.post("/graphql/", data={"query": mutation}, content_type="application/json")
    return token_response.json()["data"]["tokenAuth"]["token"]


@pytest.fixture
def auth_client(client, token):
    """Подключаем запрос с авторизацией"""
    client.defaults['HTTP_AUTHORIZATION'] = f'JWT {token}'
    return client


@pytest.mark.django_db
def test_order_from_cart_mutation(auth_client):
    """Тест на создание заказа из корзины"""
    product = Product.objects.get(pk=1)

    mutation = f"""
        mutation {{
          changeCart(productId: {product.pk}, action: "inc") {{
            ok
            cart
          }}
        }}
    """
    response = auth_client.post('/graphql/', data={'query': mutation}, content_type='application/json')

    data = response.json()
    assert 'errors' not in data
    assert data['data']['changeCart']['ok'] is True

    cart_data = json.loads(data['data']['changeCart']['cart'])

    assert str(product.pk) in cart_data
    assert cart_data[str(product.pk)]['qty'] == 1
    assert Decimal(cart_data[str(product.pk)]['price']) == product.price


    order_mutation = f"""
        mutation {{
          createOrder(address: "Mira", city: "Tver", methodId: 1, phone: "79520000000") {{
            result {{
              invoiceNumber
              id
              items {{
                price
                quantity
                product {{
                  name
                }}
              }}
            }}
          }}
        }}
    """
    response = auth_client.post('/graphql/', data={'query': order_mutation}, content_type='application/json')

    json_data = response.json()
    assert 'errors' not in json_data

    data = json_data["data"]["createOrder"]['result']

    assert data['id'] == '1'
    assert len(data['items']) == 1
    assert data['items'][0]['product']['name'] == 'Unmalted Wheat'
