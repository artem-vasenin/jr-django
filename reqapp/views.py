from django.shortcuts import render

# Create your views here.
def index(request):
    name = request.GET.get('name', 'Unknown')
    surname = request.GET.get('surname', 'Unknown')
    context = {'full_name': f'{name} {surname}'}
    return render(request, 'reqapp/index.html', context=context)
