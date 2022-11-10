from django.db import models
from django.utils.translation import gettext_lazy as _

from api.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        UNDEFINED = 'UNDEFINED', _('UNDEFINED')
        WAIT = 'WAIT', _('WAIT')
        EXPIRED = 'EXPIRED', _('EXPIRED')
        ACCEPT = 'ACCEPT', _('ACCEPT')
        DECLINE = 'DECLINE', _('DECLINE')
        LOST = 'LOST', _('LOST')

    author = models.ForeignKey(User, related_name='author_notification', null=True, on_delete=models.SET_NULL,
                               verbose_name='Автор')
    recipient = models.ForeignKey(User, related_name='recipient', null=True, on_delete=models.SET_NULL,
                                  verbose_name='Получатель')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    state = models.CharField(max_length=32, default=Type.UNDEFINED, choices=Type.choices, verbose_name='Статус')
    text = models.TextField(null=True, blank=True, verbose_name='Текст уведомления')

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
