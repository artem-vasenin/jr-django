from django import forms
from django.core.validators import RegexValidator

from orders.forms import ChoiceField
from orders.models import PaymentMethod


class UserLoginForm(forms.Form):
    """ Форма входа пользователя """
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'Email', 'id': 'email'})
    )
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Password', 'id': 'password'})
    )


class RegisterForm(forms.Form):
    """ Форма регистрации пользователя """
    username = forms.CharField(
        required=True,
        label='Login',
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Login', 'id': 'login'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'Email', 'id': 'email'})
    )
    password1 = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Password', 'id': 'password1'})
    )
    password2 = forms.CharField(
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Confirm Password', 'id': 'password2'})
    )


class AccountForm(forms.Form):
    """ Форма изменения профиля пользователя """
    first_name = forms.CharField(
        required=True,
        label='First name',
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'First name', 'id': 'first-name'})
    )
    last_name = forms.CharField(
        required=True,
        label='Last name',
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Last name', 'id': 'last-name'})
    )
    phone = forms.CharField(
        max_length=11,
        required=True,
        label='Phone',
        widget=forms.TextInput(
            attrs={'class': 'Input', 'placeholder': '79520000000', 'id': 'phone'}
        ),
        validators=[
            RegexValidator(
                regex=r'^79\d{9}$',
                message='Номер телефона должен начинаться с 79 и содержать 11 цифр, например: 79529999999',
            ),
        ]
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'Input', 'placeholder': 'my@gmail.com', 'id': 'email'}
        )
    )
    city = forms.CharField(
        required=True,
        max_length=100,
        label='City',
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'City', 'id': 'city'})
    )
    address = forms.CharField(
        required=True,
        max_length=300,
        label="Shipping address",
        widget=forms.Textarea(attrs={'class': 'Textarea', 'placeholder': 'Shipping address', 'id': 'address', 'rows': '4'})
    )
    image = forms.ImageField(
        required=False,
        label='Avatar',
        widget=forms.FileInput(
            attrs={
                'id': 'image-upload-input',
                'class': 'image-field',
                'accept': 'image/*',
            }
        ),
    )


class BalanceForm(forms.Form):
    """ Форма пополнения баланса пользователем """
    amount = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'Input',
            'placeholder': 'Price',
            'id': 'price',
            'step': '0.01',
            'min': '0',
            'max': '99999999',
        })
    )
    method = ChoiceField(
        required=True,
        queryset=PaymentMethod.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'payment-block'}),
        empty_label=None,
        label='Payment Method',
    )
