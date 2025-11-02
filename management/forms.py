from django import forms
from products.models import Category, Product


class CategoryForm(forms.ModelForm):
    """ Форма добавления/изменения категории товара менеджером """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Name', 'id': 'name'})
    )

    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='No parent',
        widget=forms.Select(attrs={'class': 'Select', 'placeholder': 'Parent', 'id': 'parent'})
    )

    class Meta:
        model = Category
        fields = ['name', 'parent']


class ProductForm(forms.ModelForm):
    """ Форма добавления/изменения товара менеджером """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Name', 'id': 'name'})
    )
    description = forms.CharField(
        max_length=9999,
        required=False,
        widget=forms.Textarea(attrs={'class': 'Textarea', 'placeholder': 'Description', 'id': 'description'})
    )
    price = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'Input',
            'placeholder': 'Price',
            'id': 'price',
            'step': '0.01',
            'min': '0',
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'Select', 'placeholder': 'Parent', 'id': 'parent'})
    )
    is_active = forms.CheckboxInput()
    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'Input', 'placeholder': 'Stock', 'id': 'stock', 'min': '0'})
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'is_active', 'stock', 'image']
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'id': 'image-upload-input',
                    'class': 'is-hidden',
                    'accept': 'image/*',
                }
            ),
        }