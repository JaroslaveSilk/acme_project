# Импортируем ClassBased Views
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown
from .models import Birthday



# Добавляем миксин первым по списку родительских классов
class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm

class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm

class BirthdayDetailView(DetailView):
    model = Birthday
    
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context 
    
# Наследуем класс от встроенного ListView
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV
    model = Birthday
    # теперь поле для сортировки, которая будет применена при выводе списка
    ordering = 'id'
    # а ткже настройки пагинации!
    paginate_by = 10


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')



# То же самое, но через view -функции, а не CBV
# from django.shortcuts import get_object_or_404, redirect, render
# from django.core.paginator import Paginator
# def birthday(request, pk=None):
#     # Добавим необязательный параметр pk для id в случае редактирования
#     if pk is not None:
#         # В случае если это редактирование - достаем объект из БД
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         # Если нет - объект не требуется
#         instance = None
#     # Привяжем объект если таковой имеется к конструктору формы
#     form = BirthdayForm(request.POST or None,
#                         # Файлы переданные в запросе указываются отдельно
#                         files=request.FILES or None,
#                         instance=instance)
#     # Создаём словарь контекста сразу после инициализации формы.
#     context = {'form': form}
#     # Если форма валидна...
#     if form.is_valid():
#         form.save()
#         # ...вызовем функцию подсчёта дней:
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)



# def birthday_list(request):
#     # Получаем список всех объектов с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаем объект пагинатора с количеством 10 записей на стр.
#     paginator = Paginator(birthdays, 10)
#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора.
#     # Если нет параметра page или он не корректен вернется 1я стр.
#     page_obj = paginator.get_page(page_number)
#     #Вместо полного списка объектов передаем в контекст объект стр пагинатора
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)


# def delete_birthday(request, pk):
#     # Получаем объект модели или выдаем ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # Для удаления параметры запроса не нужно - только удаляемый объект.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен Post-запрос
#     if request.method == 'POST':
#         instance.delete()
#         # затем переадресовываем пользователя на список записей.
#         return redirect('birthday:list')
#     return render(request, 'birthday/birthday.html', context)
