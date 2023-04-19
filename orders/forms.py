from django import forms

from billing.models import Table
from .models import TableOrder


class CreateTableOrderForm(forms.ModelForm):
    class Meta:
        model = TableOrder
        fields = ['table']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.exclude(tableorder__status__in=['pending', 'accepted'])