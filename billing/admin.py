from django.contrib import admin

from billing.models import Table


# Register your models here.
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


admin.site.register(Table, TableAdmin)
