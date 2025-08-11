from django.urls import path

from .views import index

app_name = 'graphql'

urlpatterns = [
    path('', index, name='index'),
]