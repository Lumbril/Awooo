import datetime

from django.db import models

from api.models import User


class Breed(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название породы')

    class Meta:
        db_table = 'breeds'
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Dog(models.Model):
    account = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Аккаунт владельца')
    name = models.CharField(max_length=128, verbose_name='Кличка собаки')
    avatar = models.ImageField(upload_to='media/', null=True, blank=True, verbose_name='Аватар')
    hasAvatar = models.BooleanField(verbose_name='Есть ли аватар')
    data_update_avatar = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата обновления аватара')
    breed = models.ForeignKey(Breed, null=True, on_delete=models.SET_NULL, verbose_name='Порода')
    gender = models.BooleanField(verbose_name='Пол (0 - ж, 1 - м)')
    birthday = models.DateField(verbose_name='День рождения')
    city = models.CharField(max_length=128, verbose_name='Город')
    owner = models.TextField(verbose_name='Владельцы')
    phone = models.TextField(verbose_name='Номер телефона')
    hide_phone = models.BooleanField(verbose_name='Скрыть номер')
    about = models.TextField(null=True, blank=True, verbose_name='Текст о собаке')
    food = models.TextField(null=True, blank=True, verbose_name='Информация о питании')
    other = models.TextField(null=True, blank=True, verbose_name='Другая информация')

    class Meta:
        db_table = 'dogs'
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
