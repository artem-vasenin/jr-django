from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """ Форма создания отзыва и оценки товара """
    rating = forms.ChoiceField(
        choices=[(i, '★') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'required': True})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment', 'user', 'product']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Your comment...', 'rows': 4, 'min-length': 20, 'required': True, 'class': 'Textarea'
            }),
        }