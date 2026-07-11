from django import template
from blog.models import BlogPost

register = template.Library()

@register.simple_tag
def get_recent_posts(count=3):
    """Возвращает последние опубликованные записи"""
    return BlogPost.objects.filter(is_published=True)[:count]

@register.filter
def truncate_chars(value, arg):
    """Обрезает текст до указанного количества символов"""
    if not value:
        return ''
    if len(value) <= arg:
        return value
    return value[:arg] + '...'