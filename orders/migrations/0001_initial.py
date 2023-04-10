# Generated by Django 4.2 on 2023-04-09 18:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('menu', '0001_initial'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=255)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_orders', to='billing.table')),
                ('waiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_orders', to='employees.employee')),
            ],
        ),
        migrations.CreateModel(
            name='PersonDraft',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mark', models.FloatField(blank=True, null=True)),
                ('client_comment', models.TextField(blank=True, null=True)),
                ('waiter_comment', models.TextField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tip', models.DecimalField(decimal_places=2, max_digits=10)),
                ('items', models.ManyToManyField(related_name='personal_orders', to='menu.menuitem')),
                ('parent_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_orders', to='orders.grouporder')),
                ('payment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_order', to='billing.payment')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.persondraft')),
            ],
        ),
    ]