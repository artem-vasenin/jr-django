from django.urls import path

from .views import shop_index, group_list, product_list, order_list, product_form

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='shop_index'),
    path('groups', group_list, name='group_list'),
    path('products', product_list, name='product_list'),
    path('product', product_form, name='product_form'),
    path('orders', order_list, name='order_list'),
]