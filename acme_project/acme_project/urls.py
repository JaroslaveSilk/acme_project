# Импортируем настройки проекта.
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# К импортам из django.urls добавьте импорт функции reverse_lazy
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf.urls.static import static

urlpatterns = [
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),name='registration'),
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # В конце добавляем вызов функции static().
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
