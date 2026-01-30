from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # <-- ИМПОРТИРУЕМ МИКСИН
from catalog.models import Product, Category
from catalog.forms import ProductForm

# Главная страница с пагинацией - ОБЩЕДОСТУПНАЯ
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


# Контакты с обработкой POST - ОБЩЕДОСТУПНАЯ
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


# СПИСОК всех товаров - ОБЩЕДОСТУПНЫЙ (по условию задания)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


# Детальная страница товара - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    login_url = '/users/login/'  # Куда перенаправлять неавторизованных

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Детальная информация'
        return context


# СОЗДАНИЕ товара - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


# РЕДАКТИРОВАНИЕ товара - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    pk_url_kwarg = 'product_id'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


# УДАЛЕНИЕ товара - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'


# Тестовый контроллер - ОБЩЕДОСТУПНЫЙ
class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("TEST OK - URL работает!")
