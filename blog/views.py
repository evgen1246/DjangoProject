from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        """Показываем только опубликованные записи"""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

    def get(self, request, *args, **kwargs):
        """Увеличиваем счетчик просмотров при просмотре"""
        response = super().get(request, *args, **kwargs)
        # Увеличиваем количество просмотров
        self.object.increment_views()
        return response


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:blogpost_list')

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании"""
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{self.object.title}" успешно создана!')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новой записи'
        context['button_text'] = 'Создать'
        return context


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:blogpost_list')

    def form_valid(self, form):
        """Добавляем сообщение об успешном обновлении"""
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{self.object.title}" успешно обновлена!')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование записи'
        context['button_text'] = 'Сохранить'
        return context


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')

    def delete(self, request, *args, **kwargs):
        """Добавляем сообщение об успешном удалении"""
        self.object = self.get_object()
        title = self.object.title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Запись "{title}" успешно удалена!')
        return response
