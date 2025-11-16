import time
import logging
import graphene
from decimal import Decimal
from graphql import GraphQLError
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType

from .cert_session import Cart
from products.models import Product
from .models import Order, OrderItem, Payment


logger = logging.getLogger('api_logs')


class OrderType(DjangoObjectType):
    """Тип заказа"""
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemType(DjangoObjectType):
    """Тип злемента заказа"""
    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentType(DjangoObjectType):
    """Тип платежа"""
    class Meta:
        model = Payment
        fields = '__all__'


class CartType(graphene.ObjectType):
    items = graphene.JSONString()
    total = graphene.String()


class Query(graphene.ObjectType):
    all_orders_by_user_id = graphene.List(
        OrderType,
        pk=graphene.Int(required=True),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    order_by_id = graphene.Field(OrderType, pk=graphene.Int(required=True))
    all_order_items = graphene.List(OrderItemType, pk=graphene.Int(required=True))
    all_payments = graphene.List(PaymentType, pk=graphene.Int(required=True))
    payment_by_id = graphene.Field(PaymentType, pk=graphene.Int(required=True))
    cart = graphene.Field(CartType)

    @staticmethod
    @login_required
    def resolve_all_orders_by_user_id(root, info, pk, limit=None, offset=None):
        """Получение всех заказов пользователя"""
        lst = Order.objects.filter(user_id=pk).prefetch_related('items')
        if offset is not None:
            lst = lst[offset:]
        if limit is not None:
            lst = lst[:limit]

        return lst

    @staticmethod
    @login_required
    def resolve_order_by_id(root, info, pk):
        """Получение заказа по ID"""
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            logger.error(f'Заказ (ID:{pk}) не найден')
            raise GraphQLError(f'Заказ (ID:{pk}) не найден')

    @staticmethod
    @login_required
    def resolve_all_order_items(root, info, pk):
        """Получение элементов заказа по его ID"""
        return OrderItem.objects.filter(order_id=pk)

    @staticmethod
    @login_required
    def resolve_all_payments(root, info, pk):
        """Получение всех платежей пользователя"""
        return Payment.objects.filter(user_id=pk)

    @staticmethod
    @login_required
    def resolve_payment_by_id(root, info, pk):
        """Получение платежа по ID"""
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            logger.error(f'Платеж (ID:{pk}) не найден')
            raise GraphQLError(f'Платеж (ID:{pk}) не найден')

    @staticmethod
    @login_required
    def resolve_cart(root, info):
        """Получение корзины"""
        request = info.context
        cart = Cart(request)
        items = [
            {
                'id': item['product'].id,
                'name': item['product'].name,
                'qty': item['qty'],
                'price': float(item['price']),
                'total': float(item['total_price']),
            } for item in cart.items()
        ]
        return CartType(items=items, total=cart.get_total_price())


class CreatePayment(graphene.Mutation):
    """Создание платежа пополняющего баланс"""
    class Arguments:
        amount = graphene.Decimal(required=True)
        method_id = graphene.Int(required=True)

    result = graphene.Field(PaymentType)

    @login_required
    def mutate(self, info, amount, method_id):
        user = info.context.user
        try:
            transaction_id = f'{user.pk}_{int(time.time())}'

            payment = Payment.objects.create(
                user=user,
                amount=amount,
                method_id=method_id,
                transaction_id=transaction_id,
                status='completed'
            )

            return CreatePayment(result=payment)
        except Exception as e:
            logger.error(f'Платеж не создан: {e}')
            raise GraphQLError(f"Платеж не создан: {e}")


class ChangeCart(graphene.Mutation):
    """Изменение корзины"""
    class Arguments:
        product_id = graphene.Int(required=True)
        action = graphene.String(required=False, default_value='inc')

    ok = graphene.Boolean()
    cart = graphene.JSONString()

    @login_required
    def mutate(self, info, product_id, action='inc'):
        request = info.context
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if action == 'inc':
            if product.stock >= cart.in_cart(product) + 1:
                cart.change(product)
        elif action == 'dec':
            cart.change(product, dec=True)
        elif action == 'del':
            cart.remove(product)
        else:
            logger.error(f'Неверное действие {action}')
            raise GraphQLError('Неверное действие')

        return ChangeCart(ok=True, cart=cart.cart)


class CreateOrder(graphene.Mutation):
    """Создание заказа из корзины"""
    class Arguments:
        phone = graphene.String(required=True)
        city = graphene.String(required=True)
        address = graphene.String(required=True)
        method_id = graphene.Int(required=True)

    result = graphene.Field(OrderType)

    @login_required
    def mutate(self, info, phone, city, address, method_id):
        request = info.context
        user = request.user
        cart = Cart(request)

        if not len(cart):
            logger.error('Корзина пуста')
            raise GraphQLError('Корзина пуста')

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    order_id=f'{user.pk}_{int(time.time())}',
                    status='pending',
                    user=user,
                    city=city,
                    phone=phone,
                    address=address,
                    method_id=method_id,
                )

                for p in cart.items():
                    product = p['product']
                    OrderItem.objects.create(
                        order_id=order.pk,
                        product=product,
                        quantity=p['qty'],
                        price=p['price'],
                    )
                    product.stock -= p['qty']
                    product.save(update_fields=['stock'])

                profile = getattr(user, 'profile', None)

                if profile:
                    total = Decimal(order.total_price or 0)
                    if profile.balance >= total > 0:
                        profile.balance -= total
                        profile.save(update_fields=['balance'])
                        order.status = Order.Status.PAID
                        order.save(update_fields=['status'])

                superuser = User.objects.filter(is_superuser=True).first()
                if superuser and superuser.email:
                    send_mail(
                        subject=f'Новый заказ {order.order_id}',
                        message=f'Даказ от пользователя {user.username}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[superuser.email],
                    )

                if user.email:
                    send_mail(
                        subject='Заказ создан успешно',
                        message=f'Спасибо за заказ №{order.order_id}!',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )

                cart.clear()
                logger.info(f'Заказ №{order.order_id} создан')

                return CreateOrder(result=order)
        except Exception as e:
            logger.error(f'Ошибка заказа: {e}')
            raise GraphQLError(f'Ошибка заказа: {e}')


class Mutation(graphene.ObjectType):
    create_payment = CreatePayment.Field()
    change_cart = ChangeCart.Field()
    create_order = CreateOrder.Field()
