from django.db import models
from django.conf import settings  # Добавляем для кастомного пользователя


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите наименование категории")
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True, help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование", help_text="Введите наименование продукта")
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True, help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="image/product/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="products")
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку", help_text="Введите стоимость продукта"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отметьте, чтобы продукт был виден в каталоге"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    # === ДОБАВЛЯЕМ ПОЛЯ ДЛЯ ДЗ ===
    # 1. Поле для статуса публикации (по условию)
    # Можно оставить BooleanField или сделать CharField с choices
    # Сделаем CharField как в условии
    class Status(models.TextChoices):
        MODERATION = 'MOD', 'На модерации'
        PUBLISHED = 'PUB', 'Опубликован'
        REJECTED = 'REJ', 'Отклонен'
        UNPUBLISHED = 'UNP', 'Снят с публикации'

    publication_status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.MODERATION,  # По умолчанию не опубликован
        verbose_name="Статус публикации"
    )

    # 2. Поле владельца (по условию)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем кастомного пользователя
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        # === ДОБАВЛЯЕМ КАСТОМНЫЕ ПРАВА для ДЗ ===
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Номер телефона", blank=True)
    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.CharField(max_length=30, verbose_name="ИНН")
    address = models.TextField(max_length=255, verbose_name="Адрес")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email

