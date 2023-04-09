from django.db import models
import uuid
from menu.models import MenuItem  # Import MenuItem from the Menu app
from billing.models import Table, Payment  # Import Table and Payment from the Billing app
from employees.models import Employee  # Import Employee from the Employees app


class PersonDraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class PersonalOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(MenuItem, related_name='personal_orders')
    mark = models.FloatField(null=True, blank=True)
    client_comment = models.TextField(blank=True, null=True)
    waiter_comment = models.TextField(blank=True, null=True)
    parent_order = models.ForeignKey('GroupOrder', null=True, blank=True, on_delete=models.SET_NULL, related_name='personal_orders')
    person = models.ForeignKey(PersonDraft, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tip = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.SET_NULL, related_name='personal_order')

    def __str__(self):
        return f"{self.person.title} - {self.total}"


class GroupOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='group_orders')
    waiter = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='group_orders')

    def __str__(self):
        return self.group_name