from django.contrib import admin
from .models import Product, ProductCategory, ProductOption

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    min_num = 0
    verbose_name = 'Опция товара'
    verbose_name_plural = 'Опции товара'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_store', 'updated_at')
    list_filter = ('category', 'unit')
    search_fields = ('name', 'short_desc', 'description')
    inlines = [ProductOptionInline]
    filter_horizontal = ('category',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'product')
    search_fields = ('name', 'value')
    list_filter = ('product',)
