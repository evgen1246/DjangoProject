from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(ListView):
    """
    Контроллер для отображения списка всех опубликованных записей
    """

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        """Выводим только те записи, которые имеют признак публикации (is_published=True)"""
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")


class BlogPostDetailView(DetailView):
    """
    Контроллер для отображения детальной информации о записи
    """

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "blog_post"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    """
    Контроллер для создания новой записи
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:blogpost_list")

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании"""
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{self.object.title}" успешно создана!')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание новой записи"
        context["button_text"] = "Создать"
        return context


class BlogPostUpdateView(UpdateView):
    """
    Контроллер для редактирования записи
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Добавляем сообщение об успешном обновлении"""
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{self.object.title}" успешно обновлена!')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование записи"
        context["button_text"] = "Сохранить"
        return context


class BlogPostDeleteView(DeleteView):
    """
    Контроллер для удаления записи
    """

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:blogpost_list")

    def delete(self, request, *args, **kwargs):
        """Добавляем сообщение об успешном удалении"""
        self.object = self.get_object()
        title = self.object.title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Запись "{title}" успешно удалена!')
        return response
