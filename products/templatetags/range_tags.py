# myapp/templatetags/range_tags.py
from django import template

register = template.Library()

@register.filter
def times(value):
    """ Возвращает range(value). Безопасно — если value не число, вернёт пустой список. """
    try:
        return range(int(value))
    except Exception:
        return []
