from django.contrib import admin

from api.models import Walk, Coordinate


class CoordinateInline(admin.TabularInline):
    model = Coordinate
    extra = 0


@admin.register(Walk)
class WalkAdmin(admin.ModelAdmin):
    inlines = [CoordinateInline]


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude']
