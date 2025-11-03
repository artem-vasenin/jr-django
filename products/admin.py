from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Админка для категорий """
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    ordering = ('name',)


class ReviewInline(admin.TabularInline):
    """ Встроенные отзывы прямо в карточке товара """
    model = Review
    extra = 0
    fields = ('user', 'rating', 'comment', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Админка для товаров с миниатюрами """
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'rating', 'image_preview')
    list_editable = ('price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'rating', 'image_preview')
    inlines = [ReviewInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'unit', 'price', 'stock', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def image_preview(self, obj):
        """ Показывает миниатюру в списке и карточке товара """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Превью'

    def get_queryset(self, request):
        """ Подмешиваем аннотацию рейтинга для быстрого отображения """
        qs = super().get_queryset(request)
        return qs.prefetch_related('category').prefetch_related('reviews')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Админка для отзывов """
    list_display = ('product', 'user', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)