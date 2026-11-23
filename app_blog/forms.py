from django.forms import Form, EmailField, CharField, Textarea, TextInput


class PostEmailForm(Form):
    name = CharField(
        label='',
        max_length=50,
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Имя'},
        ),
    )
    email = EmailField(
        label='',
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Мыло кто отправляет'},
        ),
    )
    email_to = EmailField(
        label='',
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Мыло кто получает'},
        ),
    )
    text = CharField(
        widget=Textarea(
            attrs={'class': 'form-control', 'rows': 5, 'cols': 50, 'placeholder': 'Сообщение'}),
        required=False,
        label='',
    )
