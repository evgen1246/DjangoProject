from django import template

register = template.Library()


@register.filter
def truncate_chars(value, arg):
    """
    Обрезает текст до указанного количества символов
    Использование: {{ value|truncate_chars:100 }}
    """
    if not value:
        return ""
    if len(value) <= arg:
        return value
    return value[:arg] + "..."


@register.simple_tag
def get_categories():
    """
    Получает список категорий
    Использование: {% get_categories as categories %}
    """
    from catalog.models import Category

    return Category.objects.all()


@register.inclusion_tag("includes/categories_menu.html")
def show_categories():
    """
    Отображает меню категорий
    Использование: {% show_categories %}
    """
    from catalog.models import Category

    categories = Category.objects.all()
    return {"categories": categories}


@register.filter()
def media_filter(path):
    """Обработка путей к медиа-файлам"""
    if path:
        return f"/media/{path}"
    return "#"
