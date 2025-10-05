from django.urls import path

from .views import (
    ManagementView, ManagementProductView, ManagementProductsView, ManagementAddProductView,
    ManagementCategoriesView, ManagementCategoryView, ManagementAddCategoryView, ManagementDeleteCategoryView,
)


urlpatterns = [
    path('', ManagementView.as_view(), name='management'),
    path('products/', ManagementProductsView.as_view(), name='management-products'),
    path('product/<int:pk>/', ManagementProductView.as_view(), name='management-product'),
    path('product/add/', ManagementAddProductView.as_view(), name='management-add-product'),
    path('categories/', ManagementCategoriesView.as_view(), name='management-categories'),
    path('category/<int:pk>/', ManagementCategoryView.as_view(), name='management-category'),
    path('category/add/', ManagementAddCategoryView.as_view(), name='management-add-category'),
    path('category/delete/<int:pk>/', ManagementDeleteCategoryView.as_view(), name='management-delete-category'),
]