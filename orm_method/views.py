from django.shortcuts import render
from orm_method.models import Worker


def index(request):
    people = Worker.objects.all()
    return render(request, 'orm_method/index.html', {'people': people})