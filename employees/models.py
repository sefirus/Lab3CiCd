from django.contrib.auth.models import User
from django.db import models
import uuid


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, null=True)
    hire_date = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    login = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=255, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Full-time'),
            ('part_time', 'Part-time'),
            ('contract', 'Contract')
        ]
    )
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name
