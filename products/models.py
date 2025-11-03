import os
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator


def product_image_path(instance, filename):
    """ Функция создания пути для картинок товаров """
    return os.path.join('products', instance.slug or 'temp', filename)

class Category(models.Model):
    """ Модель категории товаров """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='Родитель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    """ Модель товара """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    unit = models.CharField(max_length=20, verbose_name='Единицы', default='шт')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активен')
    stock = models.IntegerField(default=0, blank=True, verbose_name='Количество')
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    @property
    def rating(self):
        result = self.reviews.aggregate(avg_rating=Avg('rating'))
        return round(result['avg_rating'] or 0)

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Модель комментария и оценки товара """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='Рейтинг')
    comment = models.TextField(max_length=999, verbose_name='Комментарий')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'{self.product.name}: "{self.comment[:30]}" ({self.user.username})'


def pre_save_product_slug(sender, instance, **kwargs):
    """ сигнал добавления слага из названия товара """
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_product_slug, sender=Product)
