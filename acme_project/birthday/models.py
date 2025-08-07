from django.db import models
from django.urls import reverse

from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        help_text='Необязательное поле',
        max_length=20)
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', blank=True, upload_to='birthdays_images')
    class Meta():
        constraints = (
            # Если после описания этого ограничения не создавать миграции -
            # Оно будет работать только в админке
            # Нужно вызвать родительский clean "super().clean()"
            # В форме чтобы проверка заработала в ней
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Uniq person constraint',
            ),
        )
    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})