from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import BlogPost


class BlogPostListView(ListView):
    """
    Список статей с фильтрацией по признаку публикации.
    Показываем только статьи с is_published=True.
    """
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Опционально: добавляем пагинацию

    def get_queryset(self):
        """Переопределяем: показываем только опубликованные статьи"""
        queryset = super().get_queryset()
        return queryset.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(DetailView):
    """
    Детальная страница статьи.
    Увеличиваем счетчик просмотров при каждом открытии.
    Разрешаем доступ к неопубликованным статьям по прямому URL.
    """
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        """Позволяем доступ ко всем статьям (включая неопубликованные)"""
        return BlogPost.objects.all()

    def get_object(self, queryset=None):
        """
        Получаем статью и атомарно увеличиваем счетчик просмотров.
        Используем F() выражение для избежания race condition.
        """
        # Получаем объект без фильтрации по публикации
        queryset = queryset or self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(queryset, pk=pk)

        # Атомарное увеличение счетчика просмотров
        BlogPost.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)

        # Обновляем объект из БД, чтобы получить актуальный счетчик
        obj.refresh_from_db()
        return obj


class BlogPostCreateView(CreateView):
    """Создание новой статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением (опционально)"""
        # Можно добавить логику, например, установку автора
        # form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    """
    Редактирование статьи.
    После успешного обновления перенаправляем на детальную страницу.
    """
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        """Перенаправляем на детальную страницу отредактированной статьи"""
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        """Разрешаем редактировать все статьи"""
        return BlogPost.objects.all()


class BlogPostDeleteView(DeleteView):
    """Удаление статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        """Разрешаем удалять все статьи"""
        return BlogPost.objects.all()
