# birthday/views.py 
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

from .models import Birthday

def birthday(request, pk=None):
    # Добавим необязательный параметр pk для id в случае редактирования
    if pk is not None:
        # В случае если это редактирование - достаем объект из БД
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        # Если нет - объект не требуется
        instance = None
    # Привяжем объект если таковой имеется к конструктору формы
    form = BirthdayForm(request.POST or None, instance=instance)
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        form.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday базы данных и передаем в context
    birthdays = Birthday.objects.all()
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выдаем ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # Для удаления параметры запроса не нужно - только удаляемый объект.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен Post-запрос
    if request.method == 'POST':
        instance.delete()
        # затем переадресовываем пользователя на список записей.
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)
