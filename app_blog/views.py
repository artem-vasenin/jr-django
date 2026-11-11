from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect


def index(request):
    data = {'site': 'mysite.com'}
    return render(request, 'app_blog/index.html', context=data)


def contact(request):
    return redirect('blog:about')

