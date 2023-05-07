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
        for item in items:
            item.main_photo_path = item.photos.first().path
            item.main_photo = item.photos.first()
            print(item.main_photo_path)
    else:
        form = MenuFilterForm()

    return render(request, 'menu.html', {'categories': categories, 'items': items, 'form': form})
