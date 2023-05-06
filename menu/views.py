from django.shortcuts import render

from menu.forms import MenuFilterForm
from menu.models import MenuItem, Category
# Create your views here.


def menu(request):
    items = MenuItem.objects.filter(is_prohibited=False)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = MenuFilterForm(request.POST)
        if form.is_valid():
            selected_category = form.cleaned_data['category']
            selected_subcategory = form.cleaned_data['subcategory']
            if selected_subcategory:
                items = items.filter(category=selected_subcategory)
            elif selected_category:
                items = items.filter(category__in=[selected_category, *selected_category.children.all()])
    else:
        form = MenuFilterForm()

    return render(request, 'menu.html', {'categories': categories, 'items': items, 'form': form})
