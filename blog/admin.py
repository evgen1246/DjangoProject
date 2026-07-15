from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Настройка отображения блоговых записей в админке
    """

    list_display = ["id", "title", "created_at", "is_published", "views_count"]
    list_display_links = ["id", "title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {}
    readonly_fields = ["views_count"]
    ordering = ["-created_at"]
    fieldsets = (
        ("Основная информация", {"fields": ("title", "content", "preview")}),
        ("Статус и статистика", {"fields": ("is_published", "views_count")}),
    )
