from django.shortcuts import render
from django.http import HttpResponse

def index(_):
    return HttpResponse('Users index')
