from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'my_auth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='my_auth/login.html',
        redirect_authenticated_user=True,
    ), name='auth_login'),
]