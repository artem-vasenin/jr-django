from django.urls import path

from .views import DetailsView, GuidesView, HomeView


app_name='products'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>', DetailsView.as_view(), name='product'),
    path('guides/', GuidesView.as_view(), name='guides'),
]