from .models import Product, Category


def get_products_by_category(category_id):
    """Сервисная функция для получения списка всех продуктов в указанной категории."""
    try:
        category = Category.objects.get(pk=category_id)
        products = Product.objects.filter(
            category=category,
            is_published=True
        ).select_related('category')
        return products
    except Category.DoesNotExist:
        return Product.objects.none()


def get_category_by_id(category_id):
    """Сервисная функция для получения категории по ID."""
    try:
        return Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return None


def get_all_categories():
    """
    Сервисная функция для получения всех категорий.
    """
    return Category.objects.all()