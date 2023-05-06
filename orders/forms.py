from django import forms

from billing.models import Table
from menu.models import MenuItem
from .models import TableOrder, PersonalOrder
from django.db.models import Subquery, OuterRef


class CreateTableOrderForm(forms.ModelForm):
    table = forms.ModelChoiceField(queryset=Table.objects.none())

    class Meta:
        model = TableOrder
        fields = ['table']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the subquery to get the last TableOrder for each table
        last_order_subquery = TableOrder.objects.filter(table=OuterRef('pk')).order_by('-pending_date_time').values(
            'status')[:1]

        # Get the tables that have no TableOrders
        no_order_query = Table.objects.annotate(has_order=Subquery(last_order_subquery)).filter(has_order__isnull=True)

        # Get the tables that have the last TableOrder in Closed status
        closed_order_query = Table.objects.annotate(last_order_status=Subquery(last_order_subquery)).filter(
            last_order_status='Closed')

        # Combine the queries using OR operator
        tables = no_order_query | closed_order_query

        # Sort the tables by the pending_date_time of the last TableOrder
        tables = tables.annotate(last_order_pending_time=Subquery(
            TableOrder.objects.filter(table=OuterRef('pk'), status='Pending').order_by('-pending_date_time').values(
                'pending_date_time')[:1])).order_by('-last_order_pending_time')

        # Set the queryset of the ModelChoiceField to the selected tables
        self.fields['table'].queryset = tables


class PersonalOrderForm(forms.ModelForm):
    class Meta:
        model = PersonalOrder
        fields = ['table_order']


class AddMenuItemForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all())