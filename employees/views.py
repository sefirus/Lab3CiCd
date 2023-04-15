from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import WaiterLoginForm


def waiter_login(request):
    if request.method == 'POST':
        form = WaiterLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('employees:waiter_home')
    else:
        form = WaiterLoginForm(request)
    return render(request, 'waiter_login.html', {'form': form})


@login_required
def waiter_home(request):
    return render(request, 'waiter_home.html')
