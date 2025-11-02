from django import forms
from django.core.validators import RegexValidator

from .models import PaymentMethod


class ChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

    def prepare_value(self, value):
        return getattr(value, 'pk', value)

class OrderForm(forms.Form):
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
    method = ChoiceField(
        required=True,
        queryset=PaymentMethod.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'payment-block'}),
        empty_label=None,
        label='Payment Method',
    )