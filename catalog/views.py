from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# def home(request):
#     products = Product.objects.select_related("category").all()
#     context = {
#         "products": products,
#     }
#     return render(request, "home.html", context)
#
#
# def contacts(request):
#     return render(request, "contacts.html")
#
#
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     context = {
#         "product": product,
#     }
#     return render(request, "product_detail.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category").all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"  # Имя переменной в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        context["related_products"] = related_products
        return context


class ProductCreateView(CreateView):
    """Создание нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
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


class ProductUpdateView(UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
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


class ProductDeleteView(DeleteView):
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


class ContactsView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
