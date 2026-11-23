from django.urls import path
from app_blog import views

app_name='blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_details, name='details'),
    path('comment/<int:pk>/', views.post_comment, name='comment'),
]