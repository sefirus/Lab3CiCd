from django.contrib import admin
from .models import Category, MenuItem, Photo, Ingredient
# Register your models here.

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Photo)
admin.site.register(Ingredient)
