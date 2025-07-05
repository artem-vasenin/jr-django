from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from .models import Product, Order

@admin.action(description='Archive products')
def make_archive(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchive products')
def make_unarchive(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'price', 'short_desc', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = ('-created_at',)
    search_fields = ('name', 'description')
    actions = [make_archive, make_unarchive]
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        ('Price', {'fields': ['price', 'discount'], 'description': 'Поля относящиеся к стоимости'}),
        ('Optional', {'classes': ('collapse',), 'fields': ['archived']}),
    ]

admin.site.register(Product, ProductAdmin)

class ProductsInline(admin.TabularInline):
    # тянем только связанные с ордером продукты
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ProductsInline,)
    list_display = 'pk', 'delivery_address', 'status', 'promo_code', 'show_user'

    def get_queryset(self, request):
        # для того чтобы связанные поля не грузились к каждой записи а только 1 раз
        return Order.objects.select_related('user').prefetch_related('products')

    def show_user(self, obj: Order) -> str:
        # чтобы сделать свое отображение связанного поля юзер
        return obj.user.first_name or obj.user.username
