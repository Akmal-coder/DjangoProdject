from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from catalog.models import Product, Category  # ← ОБА МОДЕЛИ


# Контроллер главной страницы
def home(request):
    # Все товары
    all_products = Product.objects.all()

    # Простая пагинация: по 3 товара
    products_per_page = 3
    page = request.GET.get('page', 1)

    # Преобразуем страницу в число
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1

    # Вычисляем индексы
    start = (page - 1) * products_per_page
    end = start + products_per_page
    products = all_products[start:end]

    # Общее количество страниц
    total_pages = (all_products.count() + products_per_page - 1) // products_per_page

    context = {
        'products': products,
        'page': page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
    }
    return render(request, 'catalog/home.html', context)


# Контроллер страницы контактов (с обработкой POST)
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по {email}.")
    elif request.method == 'GET':
        return render(request, 'catalog/contacts.html')
    else:
        return HttpResponse("Метод не поддерживается", status=405)


def product_detail(request, product_id):
    """
    Отображает подробную информацию о конкретном товаре.
    """
    # Получаем товар по ID или показываем 404 ошибку
    product = get_object_or_404(Product, id=product_id)

    # Подготавливаем контекст для шаблона
    context = {
        'product': product,
        'title': f'{product.name} - Детальная информация'
    }

    # Отображаем шаблон с информацией о товаре
    return render(request, 'catalog/product_detail.html', context)


def product_create(request):
    """Добавление нового товара"""
    categories = Category.objects.all()

    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        purchase_price = request.POST.get("purchase_price")
        image = request.FILES.get("image")

        # Проверяем обязательные поля
        if name and category_id and purchase_price:
            try:
                category = Category.objects.get(id=category_id)

                # Создаем товар
                product = Product.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    purchase_price=purchase_price,
                    image=image
                )

                # Перенаправляем на страницу товара
                return redirect('catalog:product_detail', product_id=product.id)
            except Category.DoesNotExist:
                # Обработка ошибки, если категория не найдена
                return HttpResponse("Категория не найдена", status=400)
            except ValueError:
                # Ошибка преобразования цены
                return HttpResponse("Некорректная цена", status=400)

    # Для GET запроса показываем форму
    return render(request, "catalog/product_create.html", {"categories": categories})


def test(request):
    return HttpResponse("TEST OK - URL работает!")