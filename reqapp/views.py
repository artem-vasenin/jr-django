from django.core.files.storage.filesystem import FileSystemStorage
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

def index(request: HttpRequest) -> HttpResponse:
    name = request.GET.get('name', 'Unknown')
    surname = request.GET.get('surname', 'Unknown')
    context = {'full_name': f'{name} {surname}'}
    return render(request, 'reqapp/index.html', context=context)

def bio(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES.get('avatar')
        fs = FileSystemStorage()
        filename = fs.save(avatar.name, avatar)
        print('filename', filename)

    return render(request, 'reqapp/bio.html')