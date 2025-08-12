from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=600, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('шт', 'штуки'),
        ('л', 'литры'),
        ('мл', 'миллилитры'),
        ('т', 'тонны'),
        ('кг', 'килограммы'),
        ('г', 'граммы'),
        ('м', 'метры'),
        ('см', 'сантиметры'),
    ]

    name = models.CharField(max_length=600, unique=True, verbose_name='Название товара')
    price = models.PositiveIntegerField(verbose_name='Цена')
    short_desc = models.CharField(max_length=600, blank=True, null=True, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='шт', verbose_name='Единица измерения')
    in_store = models.PositiveIntegerField(verbose_name='Количество на складе')
    img = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    category = models.ManyToManyField(ProductCategory, blank=True, verbose_name='Категории')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class ProductOption(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название опции',)
    value = models.CharField(max_length=400, verbose_name='Значение опции',)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options', verbose_name='Товар')

    def __str__(self):
        return self.name