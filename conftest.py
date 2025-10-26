import pytest
from decimal import Decimal

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# from user.models import UserToken, UserProfile
# from accounts.models import Profile
from products.models import Product, Category, Review
from orders.models import Order, OrderItem, Payment


# ------------------------------
# USERS
# ------------------------------

@pytest.fixture
def user(db):
    """Создает обычного пользователя с профилем и нулевым балансом."""
    user = User.objects.create_user(username="testuser", password="pass123")
    # UserProfile создается автоматически через сигнал post_save
    profile = user.profile
    profile.balance = Decimal("0.0")
    profile.save()
    return user


@pytest.fixture
def user_with_balance(user):
    """Пользователь с ненулевым балансом."""
    profile = user.profile
    profile.balance = Decimal('200.00')
    profile.save()
    return user


# @pytest.fixture
# def token_factory(db):
#     """Фабрика токенов разных типов для пользователя."""
#     def create_token(user, token_type="refresh", expires_in_minutes=60):
#         expires_at = timezone.now() + timedelta(minutes=expires_in_minutes)
#         token = UserToken.objects.create(
#             user=user,
#             token_type=token_type,
#             token="token_" + token_type,
#             expires_at=expires_at
#         )
#         return token
#     return create_token


# ------------------------------
# SHOP
# ------------------------------

@pytest.fixture
def product_factory(db):
    """Фабрика продуктов с настраиваемыми параметрами."""
    def create_product(**kwargs):
        defaults = {
            "name": "Test Product",
            "description": "Описание продукта",
            "price": Decimal("100.0"),
            "unit": "шт",
            "category_id": 1,
            "image": "",
            "specs": {"color": "red", "weight": "1kg"},
            "is_active": True,
            "stock": 10,
        }
        defaults.update(kwargs)
        return Product.objects.create(**defaults)
    return create_product


@pytest.fixture
def product(product_factory):
    """Обычный продукт по умолчанию."""
    return product_factory()


@pytest.fixture
def product_in_stock():
    """Простой товар с остатком на складе"""
    return Product.objects.create(
        name="Тестовый товар",
        price=Decimal("100.0"),
        stock=10,
        unit="шт",
        specs={"color": "red"}
    )


@pytest.fixture
def make_order(db, product_factory):
    """Фабрика заказов с позициями."""
    def create_order(user, status="cart", total_price=Decimal("0"), items_count=1):
        order = Order.objects.create(user=user, status=status)
        for _ in range(items_count):
            product = product_factory()
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
        # Пересчет total_price
        if total_price is not None:
            order.total_price = Decimal(total_price)
            order.save()
        else:
            # Автопересчет суммы из OrderItem
            order.recalculate_total()
        return order
    return create_order


@pytest.fixture
def pending_order(make_order, user):
    """Заказ со статусом pending."""
    return make_order(user=user, status="pending")


@pytest.fixture
def paid_order(make_order, user_with_balance):
    """Оплаченный заказ для проверки инвойса и списания баланса."""
    order = make_order(user=user_with_balance, status="pending")
    Payment.process(order)  # предполагается, что метод списывает баланс и ставит статус paid
    order.refresh_from_db()
    return order


@pytest.fixture
def review_factory(db):
    """Фабрика отзывов."""
    def create_review(user, product, **kwargs):
        defaults = {"rating": 5, "comment": "Отличный товар!"}
        defaults.update(kwargs)
        return Review.objects.create(user=user, product=product, **defaults)
    return create_review


@pytest.fixture
def review(review_factory, user, product):
    """Простой отзыв."""
    return review_factory(user=user, product=product)
