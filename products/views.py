from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views import View


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'products/index.html')

class GuidesView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'products/guides.html')

class DetailsView(View):
    # def get(self, request: HttpRequest, pk: int) -> HttpResponse:
    def get(self, request, pk) -> HttpResponse:
        return render(request, 'products/details.html', {pk: pk})
