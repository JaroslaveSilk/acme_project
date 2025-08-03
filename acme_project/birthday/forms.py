# birthday/forms.py
from django import forms
from .models import Birthday


class BirthdayForm(forms.ModelForm):
    # Описывать поля не нужно, ведь они указываются в Мета.
    class Meta():
        # Указываем модель, на основе которой будет сттроиться форма.
        model = Birthday
        # Указываем какие поля нужно отобразить (все в данном случае)
        fields = '__all__'
        # Виджеты полей описываются также в подклассе Meta.
        widgets = {'birthday': forms.DateInput(attrs={'type':'date'})}