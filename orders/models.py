from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from products.models import Product


class PaymentMethod(models.Model):
    """ Модель метода платежа """
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Метод оплаты"
        verbose_name_plural = "Методы оплаты"

    def __str__(self):
        return self.code


class Order(models.Model):
    """ Модель заказа """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        PAID = 'paid', 'Оплачен'
        SHIPPED = 'shipped', 'Отправлен'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELED = 'canceled', 'Отменён'

    order_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='Номер заказа')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик', related_name='orders')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес доставки')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Телефон')
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='Метод')
    invoice_number = models.IntegerField(default=0, verbose_name='Инвойс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def total_price(self):
        result = self.items.aggregate(total=Sum(
                ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField())
            )
        )
        return result['total'] or 0

    def __str__(self):
        return f'Заказ от {self.created_at} - {self.user.username}'


class OrderItem(models.Model):
    """ Модель элемента заказа """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)], verbose_name='Количество')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'Продукт: {self.product.name} ({self.quantity} {self.product.unit}) - ${self.total_price}'


class Payment(models.Model):
    """ Модель платежа """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        COMPLETED = 'completed', 'Завершен'
        FAILED = 'failed', 'Отказано'
        CANCELED = 'canceled', 'Отменён'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Заказчик')
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='Метод')
    transaction_id = models.CharField(max_length=255, verbose_name='Транзакция')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f'Платёж от {self.created_at} на сумму {self.amount}'

