from django.shortcuts import render, redirect

from billing.forms import CallWaiterForm
from billing.models import Table
from orders.models import TableOrder


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
            table_number = form.cleaned_data['table_number']
            # ... rest of the view logic ...
    return redirect('billing:index_no_number')
