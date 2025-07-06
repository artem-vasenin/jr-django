from django import forms

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=10, max_value=100)
    bio = forms.CharField(widget=forms.Textarea)
    avatar = forms.ImageField(required=False)