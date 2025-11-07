import pytest
from django.contrib.auth.models import User

from accounts.models import Profile


@pytest.mark.django_db
def test_users_profile_creation():
    """ Проверка создания пользователя и его профиля """
    User.objects.create_user(username='Test', email='test@bk.ru')

    user = User.objects.get(username='Test')
    profile = user.profile

    assert User.objects.count() == 1
    assert Profile.objects.count() == 1
    assert profile.balance == 0


@pytest.mark.django_db
def test_profile_edit_creation():
    """ Проверка редактирования профиля """
    User.objects.create_user(username='Test', email='test@bk.ru')

    user = User.objects.get(username='Test')
    profile = user.profile
    profile.city = 'Moscow'
    profile.address = 'Mira'
    profile.phone = '79888888888'
    profile.save(update_fields=['city', 'address', 'phone'])

    assert profile.city == 'Moscow'
    assert profile.address == 'Mira'
    assert profile.phone == '79888888888'
