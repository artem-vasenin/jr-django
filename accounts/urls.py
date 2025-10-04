from django.urls import path

from .views import UserLoginView, UserLogoutView, RegisterView, ForgotView, AccountView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotView.as_view(), name='forgot'),
    path('', AccountView.as_view(), name='account'),
]