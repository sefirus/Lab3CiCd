from django import forms


class CallWaiterForm(forms.Form):
    table_number = forms.IntegerField(widget=forms.HiddenInput())

