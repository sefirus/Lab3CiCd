from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from orders.forms import CreateTableOrderForm
from orders.models import TableOrder, PersonalOrder


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

    if personal_order_id:
        selected_personal_order = get_object_or_404(PersonalOrder, id=personal_order_id)
    else:
        selected_personal_order = personal_orders.first() if personal_orders else None

    context = {
        'table_order': table_order,
        'personal_orders': personal_orders,
        'selected_personal_order': selected_personal_order
    }
    return render(request, 'table_order.html', context)
