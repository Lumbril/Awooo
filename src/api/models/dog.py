import datetime

from django.db import models

from api.models import User


class Breed(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название породы')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'breeds'
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Dog(models.Model):
    account = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Аккаунт владельца')
    name = models.CharField(max_length=128, verbose_name='Кличка собаки')
    avatar = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Аватар')
    has_avatar = models.BooleanField(verbose_name='Есть ли аватар')
    date_update_avatar = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления аватара')
    breed = models.ForeignKey(Breed, null=True, on_delete=models.SET_NULL, verbose_name='Порода')
    gender = models.BooleanField(verbose_name='Пол (0 - ж, 1 - м)')
    birthday = models.DateField(null=True, blank=True, verbose_name='День рождения')
    city = models.CharField(null=True, blank=True, max_length=128, verbose_name='Город')
    owner = models.TextField(null=True, blank=True, verbose_name='Владельцы')
    about = models.TextField(null=True, blank=True, verbose_name='Текст о собаке')
    food = models.TextField(null=True, blank=True, verbose_name='Информация о питании')
    other = models.TextField(null=True, blank=True, verbose_name='Другая информация')   
    date_created = models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, auto_now=True, verbose_name='Изменено')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def get_avatar(self):
        return str(self.avatar) if self.avatar else None

    class Meta:
        db_table = 'dogs'
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
