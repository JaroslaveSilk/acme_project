# birthday/views.py
from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm


def birthday(request):
    form = BirthdayForm(request.GET or None)
    if form.is_valid():
        pass
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)