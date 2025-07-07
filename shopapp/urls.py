from django.urls import path

from .views import GroupListView, ProductListView, OrderListView, ProductFormView, ShopIndexView, ProductDetailsView

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='shop_index'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/', ProductFormView.as_view(), name='product_form'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
]