from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id} - {self.name}'

class Account(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.user_id} - {self.login} / {self.password}'