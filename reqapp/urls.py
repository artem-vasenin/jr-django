from django.urls import path

from .views import index, bio

app_name = 'reqapp'

urlpatterns = [
    path('', index, name='reqapp_home'),
    path('bio', bio, name='reqapp_bio'),
]