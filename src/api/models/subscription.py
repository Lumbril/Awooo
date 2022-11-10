from django.db import models

from api.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='user', null=True, on_delete=models.SET_NULL,
                             verbose_name='Пользователь')
    subscription = models.ForeignKey(User, related_name='subscription', null=True, on_delete=models.SET_NULL,
                                     verbose_name='Подписка на')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class BlackList(models.Model):
    author = models.ForeignKey(User, related_name='author', null=True, on_delete=models.SET_NULL,
                               verbose_name='Автор')
    blocked_user = models.ForeignKey(User, related_name='blocked_user', null=True, on_delete=models.SET_NULL,
                                     verbose_name='Заблокированный пользователь')

    class Meta:
        db_table = 'blacklist'
        verbose_name = 'Пользователь в ЧС'
        verbose_name_plural = 'Черный список'
