from django.urls import path

from .views import (
    GroupListView,
    ProductListView,
    OrderListView,
    ProductCreateView,
    ShopIndexView,
    ProductDetailsView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='shop_index'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/create', ProductCreateView.as_view(), name='product_form'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
]