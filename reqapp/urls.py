from django.urls import path

from .views import index

app_name = 'reqapp'

urlpatterns = [
    path('', index, name='reqapp_home'),
]