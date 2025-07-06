from django.core import validators

from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    price = forms.IntegerField(label='Price', min_value=0, max_value=999999)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        validators=[validators.RegexValidator(
            regex=r'great',
            message='Field must contain field "great"'
        )]
    )
    discount = forms.IntegerField(label='discount', min_value=0, max_value=100)