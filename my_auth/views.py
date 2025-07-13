from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View

class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/shop/products')
        return render(request, 'my_auth/login.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/shop/products')

        return render(request, 'my_auth/login.html', {'error': 'User is not found'})

def set_cookie_view(_: HttpRequest) -> HttpResponse:
    res = HttpResponse('Added COOKIES')
    res.set_cookie('name', 'Rusich', max_age=3600)
    return res

def get_cookies_view(request: HttpRequest) -> HttpResponse:
    res = request.COOKIES.get('name', 'Default Name')
    return HttpResponse(f'{res}')

def set_session_view(request: HttpRequest) -> HttpResponse:
    res = HttpResponse('Added SESSION')
    request.session['area'] = 'Manjak'
    return res

def get_session_view(request: HttpRequest) -> HttpResponse:
    res = request.session.get('area', 'Unknown area')
    return HttpResponse(res)