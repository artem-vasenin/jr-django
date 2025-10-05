from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout

from .mixins import AnonymousRequiredMixin
from .forms import UserLoginForm, RegisterForm, AccountForm


class UserLoginView(AnonymousRequiredMixin, View):
    template_name = 'accounts/login-form.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error(None, 'Неверный email или пароль')
                return render(request, self.template_name, {'form': form})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неверный email или пароль')

        return render(request, self.template_name, {'form': form})


class RegisterView(AnonymousRequiredMixin, View):
    template_name = 'accounts/register-form.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                form.add_error(None, 'Такой email или login уже заняты')
                return render(request, self.template_name, {'form': form})

            if not password1 == password2:
                form.add_error(None, 'Ваши пароли не совпадают')
                return render(request, self.template_name, {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)

            return redirect('home')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('login')


class ForgotView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/forgot-password-form.html')


class AccountView(View):
    template_name = 'accounts/account.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        profile = user.profile if user else None
        initial = {
            'first_name': getattr(user, 'first_name', ''),
            'last_name': getattr(user, 'last_name', ''),
            'email': user.email,
            'phone': getattr(profile, 'phone', ''),
            'city': getattr(profile, 'city', ''),
            'address': getattr(profile, 'address', ''),
        }
        form = AccountForm(initial=initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            address = form.cleaned_data.get('address')

            if User.objects.filter(Q(email=email) & ~Q(pk=request.user.pk)).exists():
                form.add_error(None, 'Такой email уже занят')
                return render(request, self.template_name, {'form': form})

            if User.objects.filter(Q(profile__phone=phone) & ~Q(pk=request.user.pk)).exists():
                form.add_error(None, 'Такой телефон уже занят')
                return render(request, self.template_name, {'form': form})

            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.profile.phone = phone
            user.profile.city = city
            user.profile.address = address
            user.save()
            messages.success(request, 'Category changed successfully')

        return render(request, self.template_name, {'form': form})