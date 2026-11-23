from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
import nh3
from pymdownx.emoji import gemoji, to_alt
from copy import deepcopy

from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('app_blog/show_latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).exclude(total_comments=0).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    html = markdown.markdown(
        text,
        extensions=[
            'fenced_code',
            'nl2br',
            'pymdownx.emoji',
        ],
        extension_configs={
            'pymdownx.emoji': {
                'emoji_index': gemoji,
                'emoji_generator': to_alt,
            }
        }
    )

    attrs = deepcopy(nh3.ALLOWED_ATTRIBUTES)
    attrs.setdefault('code', set()).add('class')

    safe_html = nh3.clean(html, attributes=attrs)
    return mark_safe(safe_html)