import os
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.slug}.{ext}" if instance.slug else filename
    return os.path.join('products', instance.slug or 'temp', filename)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    name = models.CharField(max_length=100, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    stock = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def pre_save_product_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_product_slug, sender=Product)
