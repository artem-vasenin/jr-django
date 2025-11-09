import time
import graphene
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from graphene_django.types import DjangoObjectType

from .cert_session import Cart
from products.models import Product
from .models import Order, OrderItem, Payment


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
    all_orders = graphene.List(OrderType)
    order_by_id = graphene.Field(OrderType, pk=graphene.Int(required=True))
    all_order_items = graphene.List(OrderItemType, pk=graphene.Int(required=True))
    all_payments = graphene.List(PaymentType)
    payment_by_id = graphene.Field(PaymentType, pk=graphene.Int(required=True))
    cart = graphene.Field(CartType)

    @staticmethod
    def resolve_all_orders(root, info):
        """Получение всех заказов"""
        return Order.objects.prefetch_related('items')

    @staticmethod
    def resolve_order_by_id(root, info, pk):
        """Получение заказа по ID"""
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def resolve_all_order_items(root, info, pk):
        """Получение элементов заказа по его ID"""
        return OrderItem.objects.filter(order_id=pk)

    @staticmethod
    def resolve_all_payments(root, info):
        """Получение всех платежей"""
        return Payment.objects.all()

    @staticmethod
    def resolve_payment_by_id(root, info, pk):
        """Получение платежа по ID"""
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return None

    @staticmethod
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

    def mutate(self, info, amount, method_id):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Access denied")

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
            raise Exception(f"Payment was not created: {e}")


class ChangeCart(graphene.Mutation):
    """Изменение корзины"""
    class Arguments:
        product_id = graphene.Int(required=True)
        action = graphene.String(required=False, default_value='inc')

    ok = graphene.Boolean()
    cart = graphene.JSONString()

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
            raise Exception('Invalid action')

        return ChangeCart(ok=True, cart=cart.cart)


class CreateOrder(graphene.Mutation):
    """Создание заказа из корзины"""
    class Arguments:
        phone = graphene.String(required=True)
        city = graphene.String(required=True)
        address = graphene.String(required=True)
        method_id = graphene.Int(required=True)

    result = graphene.Field(OrderType)

    def mutate(self, info, phone, city, address, method_id):
        request = info.context
        user = request.user

        if not user or not user.is_authenticated:
            raise Exception('Access denied')

        cart = Cart(request)
        if not len(cart):
            raise Exception('Cart is empty')

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
                        subject=f'New order {order.order_id}',
                        message=f'Added new order from {user.username}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[superuser.email],
                    )

                if user.email:
                    send_mail(
                        subject='Your order is successful',
                        message=f'Thank you for order №{order.order_id}!',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )

                cart.clear()

                return CreateOrder(result=order)
        except Exception as e:
            raise Exception(f'Order not created: {e}')


class Mutation(graphene.ObjectType):
    create_payment = CreatePayment.Field()
    change_cart = ChangeCart.Field()
    create_order = CreateOrder.Field()
