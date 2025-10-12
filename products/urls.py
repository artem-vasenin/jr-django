from django.urls import path

from .views import DetailsView, GuidesView, HomeView, AddReviewView


app_name='products'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug>', DetailsView.as_view(), name='product'),
    path('guides/', GuidesView.as_view(), name='guides'),
    path('add-review/', AddReviewView.as_view(), name='add-review'),
]