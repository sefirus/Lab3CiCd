from django import forms

from billing.models import Table
from menu.models import MenuItem
from .models import TableOrder, PersonalOrder


class CreateTableOrderForm(forms.ModelForm):
    class Meta:
        model = TableOrder
        fields = ['table']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.exclude(tableorder__status__in=['pending', 'accepted'])


class PersonalOrderForm(forms.ModelForm):
    class Meta:
        model = PersonalOrder
        fields = ['table_order']


class AddMenuItemForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all())