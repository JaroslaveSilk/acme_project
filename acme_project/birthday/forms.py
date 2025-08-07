# birthday/forms.py
from django import forms

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Birthday


BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}

class BirthdayForm(forms.ModelForm):
    # Описывать поля не нужно, ведь они указываются в Мета.
    class Meta():
        # Указываем модель, на основе которой будет сттроиться форма.
        model = Birthday
        # Указываем какие поля нужно отобразить (все в данном случае)
        fields = '__all__'
        # Виджеты полей описываются также в подклассе Meta.
        widgets = {'birthday': forms.DateInput(attrs={'type':'date'},
                                               format='%Y-%m-%d')}
        
    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        # Вызов родительского clean() для работы ограниченияв модели БД
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии в множестве имен.
        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытается опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True
            )
            raise ValidationError(
                'Мы тоже любим Beatles, но введите, пожалйста, настоящее имя!'
            )
