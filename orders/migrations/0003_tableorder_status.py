# Generated by Django 4.2 on 2023-04-11 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_grouporder_table_remove_grouporder_waiter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending', max_length=10),
        ),
    ]
