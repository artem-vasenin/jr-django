import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def image_path(instance, filename):
    return os.path.join('accounts', instance.user.username or 'temp', filename)


class Profile(models.Model):
    """ Модель профиля пользователя с доп инфо """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес доставки')
    balance = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Баланс', blank=True, default=0)
    image = models.ImageField(upload_to=image_path, null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Телефон',
        validators=[
            RegexValidator(
                regex=r'^79\d{9}$',
                message='Номер телефона должен начинаться с 79 и содержать 11 цифр, например: 79529999999',
            ),
        ]
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' if self.user.first_name else self.user.username
