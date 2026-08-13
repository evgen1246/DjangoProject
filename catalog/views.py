from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Product
from .services import get_products_by_category, get_category_by_id, get_all_categories


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category").filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"  # Имя переменной в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        context["related_products"] = related_products
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно создан!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление товара"
        context["button_text"] = "Создать товар"
        return context

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно обновлен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование товара"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if product.owner != self.request.user and not self.request.user.is_superuser:
            messages.error(self.request, "Вы не являетесь владельцем этого товара и не можете его редактировать.")
            raise PermissionDenied
        return product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Товар "{title}" успешно удален!')
        return response

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if not (
            product.owner == self.request.user
            or self.request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user.is_superuser
        ):
            messages.error(self.request, "У вас нет прав для удаления этого товара.")
            raise PermissionDenied
        return product


class ContactsView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Отмена публикации товара (только для авторизованных с правом can_unpublish_product)"""

    model = Product
    template_name = "catalog/product_unpublish_confirm.html"
    context_object_name = "product"
    permission_required = "catalog.can_unpublish_product"
    raise_exception = False

    def post(self, request, *args, **kwargs):
        """Обработка POST запроса для отмены публикации"""
        self.object = self.get_object()
        if not self.object.is_published:
            messages.warning(self.request, f'Товар "{self.object.name}" уже снят с публикации.')
            return redirect("catalog:product_detail", pk=self.object.pk)
        self.object.is_published = False
        self.object.save()

        messages.success(self.request, f'Товар "{self.object.name}" снят с публикации!')
        return redirect("catalog:product_detail", pk=self.object.pk)

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        if product.owner != self.request.user and not self.request.user.has_perm("catalog.can_unpublish_product"):
            messages.error(self.request, "У вас нет прав для отмены публикации этого товара.")
            raise PermissionDenied
        return product


class ProductsByCategoryView(ListView):
    """
    Представление для отображения продуктов в указанной категории.
    """
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_category_by_id(category_id)
        context['category'] = category
        context['categories'] = get_all_categories()
        return context