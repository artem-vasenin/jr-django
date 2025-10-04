from django.urls import path

from .views import DetailsView, GuidesView


urlpatterns = [
    path('<int:pk>', DetailsView.as_view(), name='product'),
    path('guides/', GuidesView.as_view(), name='guides'),
]