from django.contrib import admin

from employees.models import Position


# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


admin.site.register(Position, PositionAdmin)