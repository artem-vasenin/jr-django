from django.urls import path

from .views import index

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
]