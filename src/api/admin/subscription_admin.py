from django.contrib import admin

from api.models.subscription import Subscription, BlackList


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription']
    search_fields = ['user']


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['author', 'blocked_user']
    search_fields = ['author']
