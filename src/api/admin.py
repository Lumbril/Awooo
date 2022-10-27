from django.contrib import admin

from api.models import User, Code


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'type', 'number_of_attempts']
