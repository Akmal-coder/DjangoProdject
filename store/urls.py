from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('catalog.urls', namespace='catalog')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('blogs/', include('blog.urls')),
]

