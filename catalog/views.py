from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from catalog.models import Product, Category
from catalog.forms import ProductForm

# Главная страница с пагинацией
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


# Контакты с обработкой POST
class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        """Обработка GET запроса - показ формы"""
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """Обработка POST запроса - получение данных формы"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по {email}.")


# СПИСОК всех товаров
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


# Детальная страница товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Детальная информация'
        return context


# СОЗДАНИЕ товара
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm  # <-- ВАЖНО! Используем нашу форму с валидацией!
    template_name = 'catalog/product_create.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


# РЕДАКТИРОВАНИЕ товара
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # <-- Используем ту же форму с валидацией!
    template_name = 'catalog/product_form.html'  # Можно использовать общий шаблон
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


# УДАЛЕНИЕ товара
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'  # <-- Обязательный шаблон по критериям!
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:product_list')  # После удаления - на список товаров


# 8. Тестовый контроллер
class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("TEST OK - URL работает!")