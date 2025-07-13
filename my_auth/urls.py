from django.urls import path
from django.contrib.auth.views import LoginView
from .views import get_cookies_view, set_cookie_view

app_name = 'my_auth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='my_auth/login.html',
        redirect_authenticated_user=True,
    ), name='auth_login'),
    path('get_c/', get_cookies_view, name='auth_get_c'),
    path('set_c/', set_cookie_view, name='auth_set_c'),
]