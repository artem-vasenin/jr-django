from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, created = Group.objects.get_or_create(name='profile_manager')
        perm = Permission.objects.get(codename='view_profile')
        perm_log = Permission.objects.get(codename='view_logentry')

        group.permissions.add(perm)
        user.groups.add(group)
        user.user_permissions.add(perm_log)
        group.save()
        user.save()