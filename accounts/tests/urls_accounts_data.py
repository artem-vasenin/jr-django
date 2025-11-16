from ..views import (
    UserLoginView, UserLogoutView, RegisterView, AccountBalanceView,
    AccountOrdersView, AccountProfileView, AccountSecurityView,
)
from django.contrib.auth import views as auth_views

urls = [
    # Аутентификация
    ("accounts:login", UserLoginView, "???", 200),
    ("accounts:logout", UserLogoutView, "???", 200),
    ("accounts:register", RegisterView, "???", 200),
    ("accounts:orders", AccountOrdersView, "???", 200),
    ("accounts:profile", AccountProfileView, "???", 200),
    ("accounts:security", AccountSecurityView, "???", 200),
    ("accounts:balance", AccountBalanceView, "???", 200),
    ("accounts:forgot", auth_views.PasswordResetView, "???", 200),
    ("accounts:password_reset_done", auth_views.PasswordResetDoneView, "???", 200),
    ("accounts:password_reset_complete", auth_views.PasswordResetCompleteView, "???", 200),
]