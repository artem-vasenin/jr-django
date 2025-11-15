import logging
from decimal import Decimal
from .models import Payment
from accounts.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save


logger = logging.getLogger('api_logs')


@receiver(post_save, sender=Payment)
def update_balance(sender, instance, created, **kwargs):
    """ Сигнал пополнения баланса профиля при статусе платежа Завершен """
    if instance.status == Payment.Status.COMPLETED:
        try:
            profile = Profile.objects.get(user=instance.user)
            profile.balance = (profile.balance or Decimal('0')) + instance.amount
            profile.save(update_fields=['balance'])
            logger.info(f'Баланс профиля {instance.user.username} пополнен')
        except Profile.DoesNotExist:
            logger.error(f'Профиль не найден {instance.user.username}')
