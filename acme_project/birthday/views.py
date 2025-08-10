# Импортируем ClassBased Views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView,UpdateView
)

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')

class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         # Сохраняем объект в БД.
#         congratulation.save()
#     return redirect('birthday:detail', pk=pk)
class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})

# Добавляем миксин первым по списку родительских классов
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)

class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
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
            self.object.birthday)
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context 

# Наследуем класс от встроенного ListView
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV
    model = Birthday
    # По умолчанию этот класс 
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related('tags').select_related(
        'author')
    # теперь поле для сортировки, которая будет применена при выводе списка
    ordering = 'id'
    # а ткже настройки пагинации!
    paginate_by = 10


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
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
