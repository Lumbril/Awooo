from django.db import models
from api.models import User, Dog
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
    user = models.ForeignKey(User, null=True, related_name='participant_user', on_delete=models.SET_NULL,
                             verbose_name='Пользователь')
    dog = models.ForeignKey(Dog, null=True, related_name='participant_dog', on_delete=models.SET_NULL,
                            verbose_name='Собака пользователя')

    def __str__(self):
        return f'{self.user} - {self.dog}'

    class Meta:
        db_table = 'participant'
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чатов'


class Chat(models.Model):
    participants = models.ManyToManyField(Participant, null=True, blank=True, related_name='chat_participants',
                                          db_table='chat_participant')
    date_created = models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, auto_now=True, verbose_name='Изменено')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = 'chat'
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    class Type(models.TextChoices):
        SENT = 'SENT', _('SENT')
        READ = 'READ', _('READ')

    chat = models.ForeignKey(Chat, null=True, related_name='chat', on_delete=models.SET_NULL,
                             verbose_name='Чат')
    author = models.ForeignKey(Participant, null=True, related_name='message_author', on_delete=models.SET_NULL,
                               verbose_name='Автор сообщения')
    message = models.TextField(verbose_name='Сообщение')
    state = models.CharField(max_length=32, choices=Type.choices, verbose_name='Статус')
    date_created = models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
