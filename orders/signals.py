from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Payment
from accounts.models import Profile


@receiver(post_save, sender=Payment)
def update_balance(sender, instance, created, **kwargs):
    if instance.status == Payment.Status.COMPLETED:
        try:
            profile = Profile.objects.get(user=instance.user)
            profile.balance = (profile.balance or Decimal('0')) + instance.amount
            profile.save(update_fields=['balance'])
        except Profile.DoesNotExist:
            print(f'Profile does not exsist {instance.user.username}')
