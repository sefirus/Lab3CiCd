from django.shortcuts import render, redirect, get_object_or_404

from billing.forms import CallWaiterForm, PaymentForm
from billing.models import Table
from menu.models import MenuItem, Category
from orders.models import TableOrder, Notification, GroupOrder


# Create your views here.
def index(request, table_number=None):
    request.hide_header_links = True
    if table_number is None:
        first_table = Table.objects.first()
        if first_table:
            return redirect('billing:index', table_number=first_table.number)
        else:
            # Handle the case when there are no tables in the database
            # return render(request, 'no_tables.html')
            return render(request, 'index.html', {'table': 1})

    try:
        table = Table.objects.get(number=table_number)
    except Table.DoesNotExist:
        return redirect('billing:index_no_number')

    table_order = TableOrder.objects.filter(table=table, status='Accepted').first()
    context = {
        'table': table.number,
        'table_order': table_order
    }
    return render(request, 'index.html', context)


def call_waiter(request):
    if request.method == 'POST':
        form = CallWaiterForm(request.POST)
        if form.is_valid():
            try:
                table_number = form.cleaned_data['table_number']
                table = Table.objects.get(number=table_number)

                table_order = TableOrder.objects.filter(table=table, status='Pending').first()
                if table_order:
                    target_waiter = table_order.waiter
                else:
                    target_waiter = None

                # Cancel previous notifications for the table
                Notification.objects.filter(table=table, is_cancelled=False).update(is_cancelled=True)

                # Create a new notification
                new_notification = Notification(table=table, target_waiter=target_waiter)
                new_notification.save()
                return redirect('billing:index', table_number=table.number)

            except Table.DoesNotExist:
                form.add_error(None, 'Invalid table number.')
    return redirect('billing:index_no_number')
def menu(request):
    items = MenuItem.objects.filter(is_prohibited=False)
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories, 'items': items, })


def client_checkout(request, table_number):
    request.hide_header_links = True
    table = get_object_or_404(Table,  number=table_number)
    table_order = TableOrder.objects.filter(table=table, status='Accepted').first()

    if table_order:
        unpaid_group_orders = GroupOrder.objects.prefetch_related('personal_orders__items').filter(table_order=table_order, payment=None)
        for group_order in unpaid_group_orders:
            group_order.total = sum(po.total for po in group_order.personal_orders.all())
    else:
        return redirect('billing:index', table_number)

    return render(request, 'client_checkout.html', {'unpaid_group_orders': unpaid_group_orders})


def payment(request, group_order_id):
    group_order = get_object_or_404(GroupOrder, pk=group_order_id)
    group_order.total = sum(po.total for po in group_order.personal_orders.all())

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()

            group_order.payment = payment
            group_order.save()

            # Check if all group orders are paid and close the table order if necessary
            table_order = group_order.table_order
            if all([go.payment is not None for go in table_order.group_orders.all()]):
                table_order.status = "Closed"
                table_order.save()

            return redirect("billing:client_checkout", table_order.table.number)  # or any other page you want to redirect to

    else:
        form = PaymentForm()

    context = {
        "group_order": group_order,
        "form": form,
    }

    return render(request, "payment.html", context)
