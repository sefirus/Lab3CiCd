from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from orders.forms import CreateTableOrderForm, PersonalOrderForm, AddMenuItemForm
from orders.models import TableOrder, PersonalOrder, PersonDraft, GroupOrder


# Create your views here.
@login_required
def create_table_order(request):
    request.hide_header_links = True
    request.hide_call_waiter = True

    if request.method == 'POST':
        form = CreateTableOrderForm(request.POST)
        if form.is_valid():
            table_order = form.save(commit=False)
            table_order.waiter = request.user.employee
            table_order.save()
            return redirect('employees:waiter_home')
    else:
        form = CreateTableOrderForm()
    return render(request, 'create_table_order.html', {'form': form})


@login_required
def table_order(request, table_order_id, personal_order_id=None):
    request.hide_header_links = True
    request.hide_call_waiter = True
    table_order = get_object_or_404(TableOrder, id=table_order_id)
    personal_orders = table_order.personal_orders.all()

    selected_personal_order = PersonalOrder.objects \
        .filter(id=personal_order_id) \
        .first()

    if not selected_personal_order:
        selected_personal_order = personal_orders.first() if personal_orders else None

    selected_menu_items = selected_personal_order.items.all() if selected_personal_order else []
    total = sum([item.price for item in selected_menu_items])
    add_menu_item_form = AddMenuItemForm()

    table_order_has_non_empty_personal_orders = table_order.personal_orders.filter(total__gt=0).exists()

    context = {
        'table_order': table_order,
        'personal_orders': personal_orders,
        'selected_personal_order': selected_personal_order,
        'selected_menu_items': selected_menu_items,
        'total': total,
        'add_menu_item_form': add_menu_item_form,
        'table_order_has_non_empty_personal_orders': table_order_has_non_empty_personal_orders
    }
    return render(request, 'table_order.html', context)


def get_next_person_draft_title(table_order):
    existing_personal_orders = PersonalOrder.objects \
            .filter(table_order=table_order) \
            .values_list("person__title", flat=True)
    all_persons = PersonDraft.objects.order_by('title')
    for person_draft in all_persons:
        if person_draft.title not in existing_personal_orders:
            return person_draft
    return None


@login_required
def create_personal_order(request, table_order_id):
    if request.method == 'POST':
        table_order = get_object_or_404(TableOrder, id=table_order_id)
        personal_order = PersonalOrder(table_order=table_order)
        personal_order.total = 0
        person_draft = get_next_person_draft_title(table_order)
        personal_order.person = person_draft
        personal_order.person_id = person_draft.id
        personal_order.save()
        return redirect('orders:table_order', table_order_id=table_order.id)
    else:
        # Return a 404 or any other appropriate response if the request method is not POST.
        return HttpResponseNotFound('Invalid request method')


@login_required
def add_menu_item(request, table_order_id, personal_order_id):
    if request.method == 'POST':
        form = AddMenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.cleaned_data['menu_item']
            personal_order = get_object_or_404(PersonalOrder, id=personal_order_id)
            personal_order.items.add(menu_item)
            personal_order.total = sum([item.price for item in personal_order.items.all()])
            personal_order.save()
            return redirect('orders:table_order', table_order_id=table_order_id, personal_order_id=personal_order_id)
    return HttpResponseBadRequest('Invalid form submission')


@login_required
def waiter_checkout(request, table_order_id):
    request.hide_header_links = True
    request.hide_call_waiter = True
    table_order = get_object_or_404(TableOrder, id=table_order_id)
    unprocessed_personal_orders = table_order.personal_orders.filter(total__gt=0, parent_group_order=None)
    group_orders = table_order.group_orders\
        .prefetch_related('personal_orders')\
        .prefetch_related('personal_orders__items').all()

    for group_order in group_orders:
        related_items = []
        personal_orders = group_order.personal_orders.all()
        title = ''
        for po in personal_orders:
            related_items.extend(po.items.all())
            title += po.person.title + ' '
        group_order.total = sum([item.price for item in related_items])
        group_order.title = title

    context = {
        'table_order': table_order,
        'unprocessed_personal_orders': unprocessed_personal_orders,
        'group_orders': group_orders
    }
    return render(request, 'waiter_checkout.html', context)


@login_required
def create_group_order(request, table_order_id):
    table_order = get_object_or_404(TableOrder, id=table_order_id)

    if request.method == 'POST':
        selected_personal_orders = request.POST.getlist('personal_orders')
        personal_orders = [get_object_or_404(PersonalOrder, id=po_id) for po_id in selected_personal_orders]

        group_order = GroupOrder(table_order=table_order)
        group_order.save()

        for po in personal_orders:
            group_order.personal_orders.add(po)
            po.save()

        return redirect('orders:checkout', table_order_id=table_order_id)

    return render(request, 'waiter_checkout.html', {'table_order': table_order})
