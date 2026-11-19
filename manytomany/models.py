from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} - {self.name}'

class Student(models.Model):
    name = models.CharField(max_length=30)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.id} - {self.name}'
