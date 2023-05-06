from django.shortcuts import render

from menu.models import MenuItem, Category
# Create your views here.


def menu(request):
    items = MenuItem.objects.filter(is_prohibited=False)
    categories = Category.objects.all()
    return render(request, 'menu.html', {'categories': categories, 'items': items, })
