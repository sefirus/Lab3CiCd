from django.db import models
import uuid
from menu.models import MenuItem  # Import MenuItem from the Menu app
from billing.models import Table, Payment  # Import Table and Payment from the Billing app
from employees.models import Employee  # Import Employee from the Employees app
from django.utils import timezone


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
    parent_group_order = models.ForeignKey('GroupOrder', null=True, blank=True, on_delete=models.CASCADE, related_name='personal_orders')
    person = models.ForeignKey(PersonDraft, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    table_order = models.ForeignKey('TableOrder', null=True, blank=True, related_name='personal_orders', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person.title} - {self.total}"


class GroupOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=100)
    table_order = models.ForeignKey('TableOrder', null=True, blank=True, related_name='group_orders', on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.SET_NULL, related_name='group_order')
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.group_name


class TableOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    target_waiter = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
