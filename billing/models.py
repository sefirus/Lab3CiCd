from django.db import models
import uuid


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=255,
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('cash', 'Cash'),
            ('mobile_payment', 'Mobile Payment')
        ]
    )
    payment_status = models.CharField(
        max_length=255,
        choices=[
            ('pending', 'Pending'),
            ('successful', 'Successful'),
            ('failed', 'Failed')
        ]
    )
    transaction_date = models.DateTimeField(auto_now_add=True)
