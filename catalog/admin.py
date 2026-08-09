from django.contrib import admin

from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""

    list_display = ["id", "name", "price", "category", "is_published"]
    list_display_links = ["id", "name"]
    list_filter = ["category", "is_published"]  # Фильтрация по категории
    search_fields = ["name", "description"]  # Поиск по названию и описанию
    ordering = ["id"]  # Сортировка по id
    fields = ["name", "description", "image", "category", "price", "is_published"]  # Редактирование


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""

    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "description"]
    ordering = ["name"]
