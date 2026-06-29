from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Добавление тестовых продуктов с очисткой базы данных"

    def handle(self, *args, **options):
        # Удаляем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Категории
        cat1 = Category.objects.create(name="Электроника", description="Техника и гаджеты")
        cat2 = Category.objects.create(name="Книги", description="Художественная литература")
        cat3 = Category.objects.create(name="Одежда", description="Мужская и женская одежда")

        # Продукты
        Product.objects.create(
            name="iPhone 15", description="Смартфон с отличной камерой", price=999.99, category=cat1
        )
        Product.objects.create(
            name="Ноутбук Lenovo", description="Надёжный ноутбук для работы", price=850.00, category=cat1
        )
        Product.objects.create(name="Война и мир", description="Роман Л.Н. Толстого", price=15.50, category=cat2)
