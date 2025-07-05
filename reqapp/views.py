from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

def index(request: HttpRequest) -> HttpResponse:
    name = request.GET.get('name', 'Unknown')
    surname = request.GET.get('surname', 'Unknown')
    context = {'full_name': f'{name} {surname}'}
    return render(request, 'reqapp/index.html', context=context)

def bio(request: HttpRequest) -> HttpResponse:
    return render(request, 'reqapp/bio.html')