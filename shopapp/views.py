from django.http import HttpResponse, HttpRequest

from django.shortcuts import render

def shop_index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('How are you?')
