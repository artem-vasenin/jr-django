from django.urls import path

from .views import LoginView, RegisterView, ForgotView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotView.as_view(), name='forgot'),
]