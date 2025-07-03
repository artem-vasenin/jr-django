from django.contrib import admin

from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'price', 'short_desc', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = ('-created_at',)
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'pk', 'delivery_address', 'status', 'promo_code', 'user'
