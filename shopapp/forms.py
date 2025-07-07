from django.core.exceptions import ValidationError

from django.core import validators

from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_file_name(file: InMemoryUploadedFile) -> None | ValidationError:
    name = file.name
    if name and name.count('.') == 1 and '/' not in name and '\\' not in name:
        return None
    else:
        raise ValidationError('Wrong filename')

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
    discount = forms.IntegerField(label='Discount', min_value=0, max_value=100)
    image = forms.FileField(label='Image', validators=[validate_file_name])