from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # НЕ УДАЛЯЙТЕ поле username

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Номер телефона',
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'  # Авторизация по email
    REQUIRED_FIELDS = ['username']  # username требуется для createsuperuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
