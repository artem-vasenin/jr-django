from django.db import models
from django.utils import timezone


class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.SmallIntegerField(null=True)
    created = models.DateTimeField(default=timezone.now)
    work_experience = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'#{self.id}: {self.first_name} {self.last_name}'
