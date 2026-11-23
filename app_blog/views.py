from django.shortcuts import render
from django.shortcuts import get_object_or_404
# from django.core.paginator import Paginator
from django.views.generic import ListView
from django.core.mail import send_mail
from base.env import email

from .models import Post
from .forms import PostEmailForm

class BlogListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'data'
    paginate_by = 1
    template_name = 'app_blog/list.html'

# def blog_list(request):
#     lst = Post.published.all()
#     page_num = request.GET.get('page', 1)
#     page_limit = request.GET.get('limit', 1)
#     paginator = Paginator(lst, page_limit)
#     data = paginator.get_page(page_num)
#     return render(request, 'app_blog/list.html', {'data': data})

def blog_details(request, year: int, month: int, day: int, slug: str):
    data = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    if request.method == 'POST':
        form = PostEmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email_from = form.cleaned_data['email']
            email_to = form.cleaned_data['email_to']
            text = form.cleaned_data['text']
            send_mail(
                'Глянь че!',
                f'Вот такая статейка, почитай! \nhttp://127.0.0.1:8000/{data.get_absolute_url()}\nЭто {name} [{email_from}]\n{text}',
                email,
                [email_to]
            )

    return render(
        request,
        'app_blog/details.html',
        {'data': data, 'form': PostEmailForm()}
    )
