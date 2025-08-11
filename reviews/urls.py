from django.urls import path

from .views import index

app_name = 'reviews'

urlpatterns = [
    path('', index, name='index'),
]