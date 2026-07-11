from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


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
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.select_related('category').all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'  # Имя переменной в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(
            id=product.id
        )[:4]

        context['related_products'] = related_products
        return context


class ContactsView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context