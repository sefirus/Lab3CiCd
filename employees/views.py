from datetime import datetime, timedelta
import uuid

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from orders.models import Notification, TableOrder
from .forms import WaiterLoginForm
from .models import Employee, Position


def waiter_login(request):
    request.hide_header_links = True
    request.hide_call_waiter = True
    if request.method == 'POST':
        form = WaiterLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                try:
                    Employee.objects.get(user=user)
                except Employee.DoesNotExist:
                    # Create a new Employee instance if it doesn't exist
                    employee = Employee(user=user)
                    employee.id = uuid.uuid4()
                    employee.hire_date = datetime.datetime.utcnow()
                    employee.position = Position.objects.get(title='Waiter')
                    employee.save()

                return redirect('employees:waiter_home')
    else:
        form = WaiterLoginForm(request)
    return render(request, 'waiter_login.html', {'form': form})


@login_required
def waiter_home(request):
    request.hide_header_links = True
    request.hide_call_waiter = True

    if not request.user.is_authenticated or not hasattr(request.user, 'employee'):
        return redirect('employees:waiter_login')

    cutoff_time = datetime.now() - timedelta(hours=12)
    employee = request.user.employee
    unassigned_notifications = Notification.objects\
        .filter(target_waiter=None,
                is_cancelled=False,
                created_at__gte=cutoff_time)\
        .order_by('-created_at')
    targeted_notifications = Notification.objects\
        .filter(target_waiter=employee,
                is_cancelled=False,
                created_at__gte=cutoff_time)\
        .order_by('-created_at')
    not_closed_orders = TableOrder.objects.exclude(status='Closed')
    context = {
        'unassigned_notifications': unassigned_notifications,
        'targeted_notifications': targeted_notifications,
        'not_closed_orders': not_closed_orders,
    }

    return render(request, 'waiter_home.html', context)
