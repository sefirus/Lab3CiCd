from billing.forms import CallWaiterForm


def call_waiter_form(request):
    form = CallWaiterForm()
    return {'call_waiter_form': form}