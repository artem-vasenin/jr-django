from django import forms


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