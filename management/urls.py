from django.urls import path

from .views import (
    ManagementView, ManagementProductView, ManagementProductsView, ManagementAddProductView,
    ManagementCategoriesView, ManagementCategoryView, ManagementAddCategoryView, ManagementDeleteCategoryView,
    ManagementUsersView, ManagementReviewsView,
)


app_name='management'

urlpatterns = [
    path('', ManagementView.as_view(), name='management'),
    path('products/', ManagementProductsView.as_view(), name='management-products'),
    path('product/add/', ManagementAddProductView.as_view(), name='management-add-product'),
    path('product/<slug:slug>/', ManagementProductView.as_view(), name='management-product'),
    path('categories/', ManagementCategoriesView.as_view(), name='management-categories'),
    path('category/add/', ManagementAddCategoryView.as_view(), name='management-add-category'),
    path('category/<slug:slug>/', ManagementCategoryView.as_view(), name='management-category'),
    path('category/delete/<int:pk>/', ManagementDeleteCategoryView.as_view(), name='management-delete-category'),
    path('users/', ManagementUsersView.as_view(), name='management-users'),
    path('reviews/', ManagementReviewsView.as_view(), name='management-reviews'),
]