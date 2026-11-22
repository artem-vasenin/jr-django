from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Post

def blog_list(request):
    lst = Post.published.all()
    page_num = request.GET.get('page', 1)
    page_limit = request.GET.get('limit', 1)
    paginator = Paginator(lst, page_limit)
    data = paginator.get_page(page_num)
    return render(request, 'app_blog/list.html', {'data': data})

def blog_details(request, year: int, month: int, day: int, slug: str):
    data = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )

    return render(request, 'app_blog/details.html', {'data': data})
