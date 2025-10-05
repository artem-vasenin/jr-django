from django import forms
from products.models import Category


class CategoryForm(forms.ModelForm):
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