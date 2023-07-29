from django.db import models

from api.models import User


class Walk(models.Model):
    start = models.DateTimeField(verbose_name='Время начала')
    finish = models.DateTimeField(verbose_name='Время окончания')
    time = models.IntegerField(verbose_name='Фактическое время прогулки')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    date_created = models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, auto_now=True, verbose_name='Изменено')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def __str__(self):
        walk_with_user = Walk.objects.select_related('user').get(id=self.id)

        return f'{walk_with_user.user} - {walk_with_user.start} : {walk_with_user.finish}'

    class Meta:
        db_table = 'walks'
        verbose_name = 'Прогулка'
        verbose_name_plural = 'Прогулки'


class Coordinate(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    walk = models.ForeignKey(Walk, null=True, on_delete=models.SET_NULL, verbose_name='Прогулка')

    def __str__(self):
        return f'{round(self.latitude, 2)} : {round(self.longitude, 2)}'

    class Meta:
        db_table = 'coordinates'
        verbose_name = 'GPS точка'
        verbose_name_plural = 'GPS точки'
