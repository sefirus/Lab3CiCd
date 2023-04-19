from django.shortcuts import render, redirect

from orders.forms import CreateTableOrderForm


# Create your views here.
def create_table_order(request):
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
