from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from catalog.models import Product, Category
from catalog.forms import ProductForm
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# ========== ОБЩЕДОСТУПНЫЕ ПРЕДСТАВЛЕНИЯ ==========

# Главная страница
class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context.update({
            'page': page.number,
            'total_pages': context['paginator'].num_pages,
            'has_prev': page.has_previous(),
            'has_next': page.has_next(),
        })
        return context


# Контакты
class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по {email}.")


# Список всех товаров
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


# Тестовый контроллер
class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("TEST OK - URL работает!")


# ========== ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ ==========

# Детальная страница товара
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    login_url = '/users/login/'


    @method_decorator(cache_page(60))  # Кешируем страницу на 60 секунд
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Детальная информация'
        return context


# СОЗДАНИЕ товара
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})

    # Автоматическое назначение владельца
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# РЕДАКТИРОВАНИЕ товара - ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    pk_url_kwarg = 'product_id'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})

    # Проверка что пользователь - владелец продукта
    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user


# УДАЛЕНИЕ товара - ДЛЯ ВЛАДЕЛЬЦА ИЛИ МОДЕРАТОРА
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    # Проверка что пользователь - владелец ИЛИ имеет право удалять (модератор)
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_product')


# ОТМЕНА ПУБЛИКАЦИИ - ТОЛЬКО ДЛЯ МОДЕРАТОРОВ
class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_unpublish_confirm.html'
    fields = []
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    # Проверка что пользователь имеет право can_unpublish_product
    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        form.instance.publication_status = Product.Status.UNPUBLISHED
        return super().form_valid(form)


# ПРЕДСТАВЛЕНИЕ ДЛЯ ПРОДУКТОВ В КАТЕГОРИИ

class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        # Используем сервисную функцию
        from catalog.services import get_products_by_category
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            context['category'] = category
            context['title'] = f'Продукты в категории: {category.name}'
        except Category.DoesNotExist:
            context['category'] = None
            context['title'] = 'Категория не найдена'
        return context