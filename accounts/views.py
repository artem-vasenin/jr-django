from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views import View


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/login-form.html')

class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/register-form.html')

class ForgotView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/forgot-password-form.html')

class AccountView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/account.html')
