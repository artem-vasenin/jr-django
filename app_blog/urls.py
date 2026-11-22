from django.urls import path
from app_blog import views

app_name='blog'

urlpatterns = [
    path('', views.blog_list, name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_details, name='details'),
]