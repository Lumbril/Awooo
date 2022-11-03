from django.contrib import admin
from django.utils.html import format_html

from api.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'type', 'number_of_attempts']


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'name', 'breed', 'gender', 'city']
    fields = ['account', 'name', 'avatar', 'preview', 'hasAvatar',
              'breed', 'gender', 'birthday',
              'city', 'owner', 'phone', 'hide_phone', 'about', 'food', 'other']
    readonly_fields = ['preview']

    def preview(self, obj):
        return format_html(
            '<a href="/{0}" target="_blank">'
            '<img src="/{0}" height="100"></a>', obj.get_avatar()) if obj.get_avatar() else '-'
