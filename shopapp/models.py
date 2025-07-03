from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=False, blank=True)
    discount = models.SmallIntegerField(default=0)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def short_desc(self):
        return self.description if len(self.description) < 48 else f'{self.description[:48]}...'

    def __str__(self):
        return self.name

class Order(models.Model):
    class Meta:
        ordering = ['-id']

    delivery_address = models.TextField(null=False, blank=True)
    promo_code = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=False, default="Pending")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
