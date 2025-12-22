from tkinter.constants import CASCADE

from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]

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
