from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import UserLoginForm, RegisterForm, AccountForm
from .mixins import AnonymousRequiredMixin


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

            user_with_email = User.objects.get(email=email)
            user_with_phone = User.objects.get(profile__phone=phone)

            if user_with_email and not user_with_email.pk == request.user.pk:
                form.add_error(None, 'Такой email уже занят')
                return render(request, self.template_name, {'form': form})

            if user_with_phone and not user_with_phone.pk == request.user.pk:
                form.add_error(None, 'Такой телефон уже занят')
                return render(request, self.template_name, {'form': form})

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.profile.phone = phone
            request.user.profile.city = city
            request.user.profile.address = address
            request.user.save()

        return render(request, self.template_name, {'form': form})