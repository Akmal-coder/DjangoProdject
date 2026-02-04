from django.core.cache import cache
from catalog.models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция для получения всех продуктов в указанной категории.
    Возвращает QuerySet продуктов.
    """
    try:
        category = Category.objects.get(id=category_id)
        return Product.objects.filter(category=category, is_published=True)
    except Category.DoesNotExist:
        return Product.objects.none()