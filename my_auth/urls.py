from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    get_cookies_view, set_cookie_view, set_session_view, get_session_view, logout_view, AboutView,
    RegView,
)

app_name = 'my_auth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='my_auth/login.html',
        redirect_authenticated_user=True,
    ), name='auth_login'),
    path('logout/', logout_view, name='auth_logout'),
    path('reg/', RegView.as_view(), name='reg'),
    path('about/', AboutView.as_view(), name='about'),
    path('get_c/', get_cookies_view, name='auth_get_c'),
    path('set_c/', set_cookie_view, name='auth_set_c'),
    path('get_s/', get_session_view, name='auth_get_s'),
    path('set_s/', set_session_view, name='auth_set_s'),
]