from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта с валидацией запрещенных слов"""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название товара"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "placeholder": "Введите описание товара"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
        }
        labels = {
            "name": "Название товара",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена (₽)",
        }
        help_texts = {
            "name": "Введите название товара (не более 200 символов)",
            "description": "Введите описание товара",
            "price": "Цена в рублях, например: 99.99",
        }

    def clean_name(self):
        """
        Проверка названия на наличие запрещенных слов
        """
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f'Название содержит запрещенное слово: "{word}". ' f"Пожалуйста, измените название."
                    )
        return name

    def clean_description(self):
        """
        Проверка описания на наличие запрещенных слов
        """
        description = self.cleaned_data.get("description")
        if description:
            description_lower = description.lower()
            found_words = []
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    found_words.append(word)

            if found_words:
                raise ValidationError(
                    f'Описание содержит запрещенные слова: {", ".join(found_words)}. '
                    f"Пожалуйста, удалите их из описания."
                )
        return description

    def clean_price(self):
        """
        Проверка цены: цена не может быть отрицательной
        """
        price = self.cleaned_data.get("price")
        if price is None:
            raise ValidationError("Цена не может быть пустой.")
        if price < 0:
            raise ValidationError(
                "Цена не может быть отрицательной. " "Пожалуйста, введите корректную цену (0 или больше)."
            )
        if price > 9999999.99:
            raise ValidationError("Цена слишком высокая. " "Пожалуйста, введите корректную цену.")

        return price
