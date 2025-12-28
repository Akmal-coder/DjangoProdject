from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductCreateView,
    TestView
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('test/', TestView.as_view(), name='test'),
]

# Добавляем обслуживание медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)