from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from catalog.models import Product, Category


# 1. Главная страница с пагинацией
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


# 2. Контакты с обработкой POST
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


# 3. Детальная страница товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Детальная информация'
        return context


# 4. Создание товара
class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_create.html'
    fields = ['name', 'description', 'category', 'purchase_price', 'image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


# 5. Тестовый контроллер
class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("TEST OK - URL работает!")