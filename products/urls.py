from django.urls import path

from .views import DetailsView


urlpatterns = [
    path('<int:pk>', DetailsView.as_view(), name='product'),
]