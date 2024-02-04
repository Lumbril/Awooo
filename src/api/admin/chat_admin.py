from django.contrib import admin

from api.models import Message, Chat, Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'dog']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_created', 'date_edited', 'date_deleted']
    readonly_fields = ['date_created']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'author', 'state', 'date_created']
    readonly_fields = ['date_created']
