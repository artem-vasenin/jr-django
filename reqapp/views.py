from django.core.files.storage.filesystem import FileSystemStorage
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from .forms import UserBioForm

def index(request: HttpRequest) -> HttpResponse:
    name = request.GET.get('name', 'Unknown')
    surname = request.GET.get('surname', 'Unknown')
    context = {'full_name': f'{name} {surname}'}
    return render(request, 'reqapp/index.html', context=context)

def bio(request: HttpRequest) -> HttpResponse:
    context = {'form': UserBioForm()}
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES.get('avatar')
        fs = FileSystemStorage()
        fs.save(avatar.name, avatar)

    return render(request, 'reqapp/bio.html', context=context)