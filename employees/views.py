import datetime
import uuid

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
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


@login_required
def waiter_home(request):
    return render(request, 'waiter_home.html')
