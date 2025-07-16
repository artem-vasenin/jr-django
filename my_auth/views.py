from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View
from django.urls import reverse_lazy

from .models import Profile

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

class RegView(CreateView):
    form_class = UserCreationForm
    template_name = 'my_auth/reg.html'
    success_url = reverse_lazy('my_auth:about')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        user = authenticate(
            self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1'),
        )
        login(self.request, user=user)
        return response

class AboutView(TemplateView):
    template_name = 'my_auth/about.html'

@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/auth/login')

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