# Импортируем настройки проекта.
from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # В конце добавляем вызов функции static().
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
