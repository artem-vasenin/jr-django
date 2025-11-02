from decimal import Decimal
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .models import Profile
from orders.models import Order


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Сигнал создания профиля при регистрации пользователя """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ Сигнал сохранения профиля при сохранении юзера """
    instance.profile.save()


@receiver(post_save, sender=Profile)
def orders_paid(sender, instance, created, **kwargs):
    """ Сигнал для того, чтобы при пополнении баланса оплачивать заказы """
    if created:
        return

    profile = instance
    balance = profile.balance or Decimal('0')

    with transaction.atomic():
        pending_orders = (
            Order.objects
                .filter(user=profile.user, status=Order.Status.PENDING)
                .order_by('created_at')
        )
        for o in pending_orders:
            total = Decimal(o.total_price or 0)
            if balance >= total:
                o.status = Order.Status.PAID
                o.save(update_fields=['status'])
                balance -= total
            else:
                break

        Profile.objects.filter(pk=profile.pk).update(balance=balance)