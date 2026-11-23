# from django.db.models import Model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
# from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

from base.env import email
from django.views.decorators.http import require_POST

from .models import Post, Comment
from .forms import PostEmailForm, CommentForm

# class BlogListView(ListView):
#     queryset = Post.objects.all()
#     context_object_name = 'data'
#     paginate_by = 3
#     template_name = 'app_blog/list.html'

def blog_list(request, tag_slug=None):
    lst = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        lst = lst.filter(tags=tag)
    page_num = request.GET.get('page', 1)
    page_limit = request.GET.get('limit', 3)
    paginator = Paginator(lst, page_limit)
    data = paginator.get_page(page_num)
    return render(
        request,
        'app_blog/list.html',
        {'data': data, 'tag': tag},
    )

def blog_details(request, year: int, month: int, day: int, slug: str):
    data = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    post_tags_ids = data.tags.values_list('id', flat=True)
    filtered_data = Post.published.filter(tags__in=post_tags_ids).exclude(id=data.id)
    filtered_data = filtered_data.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
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
                [email_to],
            )

    return render(
        request,
        'app_blog/details.html',
        {
            'data': data,
            'comments': data.comments.all(),
            'form': PostEmailForm(),
            'commentForm': CommentForm(),
            'filtered_data': filtered_data,
        }
    )

@require_POST
def post_comment(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return redirect(post.get_absolute_url())
