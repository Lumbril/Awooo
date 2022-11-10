from django.contrib import admin

from api.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['author', 'recipient', 'state', 'date_created']
    fields = ['author', 'recipient', 'date_created', 'state', 'text']
    readonly_fields = ['date_created']
