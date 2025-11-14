from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    UserLoginView, UserLogoutView, RegisterView, AccountBalanceView,
    AccountOrdersView, AccountProfileView, AccountSecurityView,
)

app_name='accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('orders/', AccountOrdersView.as_view(), name='orders'),
    path('profile/', AccountProfileView.as_view(), name='profile'),
    path('security/', AccountSecurityView.as_view(), name='security'),
    path('balance/', AccountBalanceView.as_view(), name='balance'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='accounts/forgot-password-form.html',
            email_template_name='accounts/forgot-password-email.html',
            subject_template_name='accounts/forgot-password-subject.txt',
            success_url=reverse_lazy('accounts:password_reset_done'),
        ),
        name='forgot',
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/forgot-password-reset-done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/forgot-password-reset-confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/forgot-password-reset-complete.html',
        ),
        name='password_reset_complete',
    ),
]