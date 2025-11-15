import time
import logging
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout

from .mixins import AnonymousRequiredMixin, AuthenticatedRequiredMixin
from .forms import UserLoginForm, RegisterForm, AccountForm, BalanceForm, ChangePasswordForm
from orders.models import Order, PaymentMethod, Payment


logger = logging.getLogger('logs')


class UserLoginView(AnonymousRequiredMixin, View):
    """ Контроллер аутентификации пользователя """
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
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                form.add_error(None, 'Неверный email или пароль')
                logger.error(f'Авторизация: Неверный email или пароль {email}')

                return render(request, self.template_name, {'form': form})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                logger.info(f'Авторизация: Вход пользователя {user.get_username()}')

                return redirect('home')
            else:
                form.add_error(None, 'Неверный email или пароль')
                logger.error(f'Авторизация: Неверный email или пароль {email}')

        return render(request, self.template_name, {'form': form})


class RegisterView(AnonymousRequiredMixin, View):
    """ Контроллер регистрации пользователем """
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
                logger.error(f'Регистрация: Такой email или login уже заняты {email}, {login}')

                return render(request, self.template_name, {'form': form})

            if not password1 == password2:
                form.add_error(None, 'Ваши пароли не совпадают')
                logger.error(f'Регистрация: Пароли не совпадают')

                return render(request, self.template_name, {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password1)
            logger.info(f'Регистрация: Пользователь зарегистрирован {user.get_username()}')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('home')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    """ Контроллер выхода пользователя """
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)

        return redirect('accounts:login')


class AccountBalanceView(View):
    """ Контроллер пополнения баланса пользователя """
    template_name = 'accounts/balance.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        first_method = PaymentMethod.objects.first()
        form = BalanceForm(initial={
            'method': first_method.pk if first_method else None
        })

        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = BalanceForm(request.POST)

        if form.is_valid():
            try:
                transaction_id = f'{request.user.pk}_{int(time.time())}'
                amount = form.cleaned_data.get('amount')
                method = form.cleaned_data.get('method')

                Payment.objects.create(
                    user=request.user,
                    amount=amount,
                    method=method,
                    transaction_id=transaction_id,
                    status='completed'
                )

                messages.success(request, f'Payment #{transaction_id} created')
                logger.info(f'Пополнение: транзакция - {transaction_id}')

                return redirect('accounts:profile')
            except Exception as e:
                logger.error(f'Пополнение: Ошибка {e}')
                messages.error(request, 'Платеж не создан')

        return render(request, self.template_name, {'form': form})


class AccountOrdersView(AuthenticatedRequiredMixin, View):
    """ Контроллер списка заказов пользователя """
    template_name = 'accounts/account-orders.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        page_number = request.GET.get('page', 1)
        per_page = 10
        orders = Order.objects.filter(user_id=user.pk).order_by('-created_at')
        paginator = Paginator(orders, per_page)
        page_obj = paginator.get_page(page_number)

        ctx = {
            'orders': page_obj,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page': f'?page={page_obj.next_page_number()}' if page_obj.has_next() else None,
            'previous_page': f'?page={page_obj.previous_page_number()}' if page_obj.has_previous() else None,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        }

        return render(request, self.template_name, ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        order_id = int(request.POST.get('id'))

        if order_id:
            order = Order.objects.filter(pk=order_id).first()

            if order:
                order.status = Order.Status.CANCELED
                order.save(update_fields=['status'])
                request.user.profile.balance += order.total_price
                request.user.profile.save(update_fields=['balance'])
                items = order.items.all()

                for i in items:
                    product = i.product
                    product.stock += i.quantity
                    product.save(update_fields=['stock'])

        return redirect('accounts:orders')


class AccountProfileView(AuthenticatedRequiredMixin, View):
    """ Контроллер изменения данных профиля пользователя """
    template_name = 'accounts/account-profile.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        profile = getattr(user, 'profile', None)
        initial = {
            'first_name': getattr(user, 'first_name', ''),
            'last_name': getattr(user, 'last_name', ''),
            'email': user.email,
        }

        if profile:
            initial['phone'] = getattr(profile, 'phone', '')
            initial['city'] = getattr(profile, 'city', '')
            initial['address'] = getattr(profile, 'address', '')

        form = AccountForm(initial=initial)
        ctx = {'form': form}

        return render(request, self.template_name, ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        form_profile = AccountForm(request.POST, request.FILES)

        if form_profile.is_valid():
            first_name = form_profile.cleaned_data.get('first_name')
            last_name = form_profile.cleaned_data.get('last_name')
            email = form_profile.cleaned_data.get('email')
            phone = form_profile.cleaned_data.get('phone')
            city = form_profile.cleaned_data.get('city')
            address = form_profile.cleaned_data.get('address')
            image = form_profile.cleaned_data.get('image')

            if User.objects.filter(Q(email=email) & ~Q(pk=request.user.pk)).exists():
                form_profile.add_error(None, 'Такой email уже есть')
                logger.error(f'Профиль: Такой email ({email}) уже есть')

                return render(request, self.template_name, {'form': form_profile})

            if User.objects.filter(Q(profile__phone=phone) & ~Q(pk=request.user.pk)).exists():
                form_profile.add_error(None, 'Такой телефон уже существует')
                logger.error(f'Профиль: Такой телефон ({phone}) уже есть')

                return render(request, self.template_name, {'form': form_profile})

            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.profile.phone = phone
            user.profile.city = city
            user.profile.address = address

            if image:
                user.profile.image = image

            user.save()
            messages.success(request, 'Профиль успешно изменен')
            logger.info(f'Профиль: Профиль успешно изменен')

            return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form_profile})


class AccountSecurityView(AuthenticatedRequiredMixin, View):
    """ Контроллер изменения пароля пользователя """
    template_name = 'accounts/account-security.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form_password = ChangePasswordForm()
        ctx = {'form': form_password}

        return render(request, self.template_name, ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        form_password = ChangePasswordForm(request.POST)

        if form_password.is_valid():
            password1 = form_password.cleaned_data.get('password1')
            password2 = form_password.cleaned_data.get('password2')

            if request.user.check_password(password1):
                request.user.set_password(password2)
                request.user.save()
                messages.success(request, 'Пароль успешно изменен')
                logger.info('Профиль: Пароль успешно изменен')

                return redirect('accounts:login')
            else:
                messages.error(request, 'Пароль изменить не удалось')
                logger.error('Профиль: Пароль изменить не удалось')

        return render(request, self.template_name, {'form': form_password})
