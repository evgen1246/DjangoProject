from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ['id', 'name', 'price', 'category']
    list_display_links = ['id', 'name']
    list_filter = ['category']  # Фильтрация по категории
    search_fields = ['name', 'description']  # Поиск по названию и описанию
    ordering = ['id']  # Сортировка по id


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'description']
    ordering = ['name']

