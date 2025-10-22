from django import forms
from django.core.validators import RegexValidator

from .models import Profile


class UserLoginForm(forms.Form):
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
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Phone', 'id': 'phone'}),
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
        widget=forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'Email', 'id': 'email'})
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
        label='Avatar',
        widget=forms.FileInput(
            attrs={
                'id': 'image-upload-input',
                'class': 'image-field',
                'accept': 'image/*',
            }
        ),
    )
