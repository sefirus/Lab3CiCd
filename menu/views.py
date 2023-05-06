from django.shortcuts import render

from menu.forms import MenuFilterForm
from menu.models import MenuItem, Category
# Create your views here.


def menu(request):
    items = MenuItem.objects.filter()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = MenuFilterForm(request.POST)
        if form.is_valid():
            selected_categories = form.cleaned_data['category']
            selected_subcategories = form.cleaned_data['subcategory']
            if selected_subcategories:
                items = items.filter(category__in=selected_subcategories)
            elif selected_categories:
                children = []
                for sc in selected_categories:
                    c = sc.children.all()
                    children.extend(c)
                children.extend(selected_categories.all())
                items = items.filter(category__in=children)
    else:
        form = MenuFilterForm()

    return render(request, 'menu.html', {'categories': categories, 'items': items, 'form': form})
