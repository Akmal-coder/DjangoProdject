from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    ContactsView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    TestView
)

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', HomeView.as_view(), name='home'),

    # Контакты
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # CRUD для продуктов (ВСЕ 5 операций)
    path('products/', ProductListView.as_view(), name='product_list'),  # СПИСОК
    path('product/create/', ProductCreateView.as_view(), name='product_create'),  # СОЗДАНИЕ
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),  # ПРОСМОТР
    path('product/<int:product_id>/update/', ProductUpdateView.as_view(), name='product_update'),  # РЕДАКТИРОВАНИЕ
    path('product/<int:product_id>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # УДАЛЕНИЕ

    # Тестовый URL
    path('test/', TestView.as_view(), name='test'),
]

# Добавляем обслуживание медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)