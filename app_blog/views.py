from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post

def blog_list(request):
    data = Post.published.all()
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
