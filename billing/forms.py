from django import forms

from billing.models import Payment


class CallWaiterForm(forms.Form):
    table_number = forms.IntegerField(widget=forms.HiddenInput())


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
        }
