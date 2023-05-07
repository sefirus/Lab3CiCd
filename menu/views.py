from django.shortcuts import render, get_object_or_404

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
            selected_tags = form.cleaned_data['tags']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']

            if selected_subcategories:
                items = items.filter(category__in=selected_subcategories)
            elif selected_categories:
                children = []
                for sc in selected_categories:
                    c = sc.children.all()
                    children.extend(c)
                children.extend(selected_categories.all())
                items = items.filter(category__in=children)

            if selected_tags:
                items = items.filter(tags__in=selected_tags)

            if min_price:
                items = items.filter(price__gte=min_price)

            if max_price:
                items = items.filter(price__lte=max_price)
    else:
        form = MenuFilterForm()

    return render(request, 'menu.html', {'categories': categories, 'items': items, 'form': form})


def menu_item(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    return render(request, 'menu_item.html', {'item': item})
