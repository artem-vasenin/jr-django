from django.urls import path

from .views import ManagementView, ManagementProductView, ManagementProductsView, ManagementAddProductView


urlpatterns = [
    path('', ManagementView.as_view(), name='management'),
    path('products/', ManagementProductsView.as_view(), name='management-products'),
    path('product/<int:pk>/', ManagementProductView.as_view(), name='management-product'),
    path('add/', ManagementAddProductView.as_view(), name='management-add'),
]