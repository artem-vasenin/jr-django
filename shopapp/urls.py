from django.urls import path

from .views import shop_index, group_list

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='shop_index'),
    path('groups', group_list, name='group_list'),
]