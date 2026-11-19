from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.id} - {self.name}:{self.company_id} ({self.price})'