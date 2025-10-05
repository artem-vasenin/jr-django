from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='City')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Shipping address')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Phone number',
        validators=[
            RegexValidator(
                regex=r'^79\d{9}$',
                message='Номер телефона должен начинаться с 79 и содержать 11 цифр, например: 79529999999',
            ),
        ]
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' if self.user.first_name else self.user.username
