import datetime
import uuid

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from orders.models import Notification, TableOrder
from .forms import WaiterLoginForm
from .models import Employee, Position


def waiter_login(request):
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


def is_waiter(user: User):
    if user.employee:
        return True
    else:
        return False


@login_required
@user_passes_test(is_waiter)
def waiter_home(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'employee'):
        return redirect('employees:waiter_login')

    employee = request.user.employee
    unassigned_notifications = Notification.objects.filter(target_waiter=None, is_cancelled=False).order_by('-created_at')
    targeted_notifications = Notification.objects.filter(target_waiter=employee, is_cancelled=False).order_by('-created_at')
    not_closed_orders = TableOrder.objects.exclude(status='closed')
    context = {
        'unassigned_notifications': unassigned_notifications,
        'targeted_notifications': targeted_notifications,
        'not_closed_orders': not_closed_orders,
    }

    return render(request, 'waiter_home.html', context)
