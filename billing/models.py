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
    transaction_id = models.CharField(max_length=255, unique=True)
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
    payer_name = models.CharField(max_length=255)
    payer_email = models.EmailField()
    payer_phone = models.CharField(max_length=255)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    card_brand = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.payment_status}"