from django.shortcuts import render, redirect

from billing.forms import CallWaiterForm
from billing.models import Table
from orders.models import TableOrder, Notification
from menu.models import MenuItem, Category


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

    table_order = TableOrder.objects.filter(table=table, status='accepted').first()
    return render(request, 'index.html', {'table': table.number, 'table_order': table_order})





def call_waiter(request):
    if request.method == 'POST':
        form = CallWaiterForm(request.POST)
        if form.is_valid():
            try:
                table_number = form.cleaned_data['table_number']
                table = Table.objects.get(number=table_number)

                table_order = TableOrder.objects.filter(table=table, status='pending').first()
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
