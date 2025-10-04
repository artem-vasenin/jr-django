from django.urls import path

from .views import LoginView, RegisterView, ForgotView, AccountView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotView.as_view(), name='forgot'),
    path('', AccountView.as_view(), name='account'),
]