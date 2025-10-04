from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'orders/index.html')
