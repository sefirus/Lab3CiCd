from django.contrib import admin

from orders.models import PersonDraft


# Register your models here.
class PersonDraftAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(PersonDraft, PersonDraftAdmin)
