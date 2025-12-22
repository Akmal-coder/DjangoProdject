from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'catalog'  # Namespace

urlpatterns = [
    path('', views.home, name='home'),  # /catalog/ -> home
    path('contacts/', views.contacts, name='contacts'),  # /catalog/contacts/ -> contacts
    # -----------------------------------------------------------------
    # ЗАДАНИЕ 1: Добавляем маршрут для страницы товара
    # -----------------------------------------------------------------
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    # Пример: /catalog/product/1/ - товар с ID=1
    # Пример: /catalog/product/2/ - товар с ID=2
    path('test/', views.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)