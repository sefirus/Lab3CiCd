# Generated by Django 4.2 on 2023-04-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_tableorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('checkout in progress', 'Checkout In Progress'), ('accepted', 'Accepted'), ('closed', 'Closed')], default='pending', max_length=25),
        ),
    ]
