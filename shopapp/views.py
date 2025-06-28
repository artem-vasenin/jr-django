from django.http import HttpResponse, HttpRequest
from datetime import datetime

from django.shortcuts import render

def shop_index(request: HttpRequest) -> HttpResponse:
    context = {"date": datetime.now()}
    return render(request, 'shopapp/index.html', context)
