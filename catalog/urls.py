from django.urls import path, include
from tomlkit import document

from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'  # Namespace

urlpatterns = [
    path('', views.home, name='home'),  # /catalog/ -> home
    path('contacts/', views.contacts, name='contacts'),  # /catalog/contacts/ -> contacts
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)