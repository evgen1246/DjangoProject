from django.db import models


class Product(models.Model):
    """Модель товара"""

    objects = None
    name = models.CharField(max_length=200, verbose_name="Наименование", help_text="Введите название товара")
    description = models.TextField(verbose_name="Описание", help_text="Введите описание товара")
    image = models.ImageField(
        upload_to="photo", verbose_name="Изображение", help_text="Загрузите изображение товара", blank=True, null=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products",  # позволяет обращаться category.products.all()
        help_text="Выберите категорию товара",
    )
    price = models.DecimalField(
        max_digits=10,  # всего цифр
        decimal_places=2,  # знаков после запятой
        verbose_name="Цена за покупку",
        help_text="Введите цену товара (в рублях)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"  # автоматически устанавливается при создании
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"  # автоматически обновляется при каждом сохранении
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]  # сортировка по дате создания (новые сверху)
        indexes = [
            models.Index(fields=["name"]),  # индекс для ускорения поиска по имени
            models.Index(fields=["category"]),  # индекс для ускорения фильтрации
        ]

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Category(models.Model):
    """Модель категории товаров"""

    objects = None
    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите название категории")
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # сортировка по имени

    def __str__(self):
        return self.name
