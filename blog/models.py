from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок записи"
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое записи"
    )
    preview = models.ImageField(
        upload_to="blog_previews/",
        verbose_name="Превью (изображение)",
        help_text="Загрузите изображение для превью",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отметьте, чтобы опубликовать запись"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Количество просмотров записи"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для просмотра записи"""
        return reverse('blog:blogpost_detail', kwargs={'pk': self.pk})

    def increment_views(self):
        """Увеличивает счетчик просмотров на 1"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


