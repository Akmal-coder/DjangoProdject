from django.urls import path
from . import views

app_name = 'catalog'  # Namespace

urlpatterns = [
    path('', views.home, name='home'),  # /catalog/ -> home
    path('contacts/', views.contacts, name='contacts'),  # /catalog/contacts/ -> contacts
]