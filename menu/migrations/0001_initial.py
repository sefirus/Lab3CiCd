# Generated by Django 4.2 on 2023-04-09 12:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.category')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('weight_grams', models.IntegerField()),
                ('fat_grams', models.IntegerField()),
                ('carbohydrate_grams', models.IntegerField()),
                ('protein_grams', models.IntegerField()),
                ('is_vegan', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('total_weight_grams', models.IntegerField()),
                ('total_calories', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_prohibited', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='menu.category')),
                ('ingredients', models.ManyToManyField(related_name='menu_items', to='menu.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('path', models.ImageField(upload_to='menu_photos/')),
                ('alt_text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemsTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menuitem')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.tags')),
            ],
            options={
                'unique_together': {('tag', 'menu_item')},
            },
        ),
        migrations.AddField(
            model_name='menuitem',
            name='photos',
            field=models.ManyToManyField(related_name='menu_items', to='menu.photo'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='tags',
            field=models.ManyToManyField(related_name='menu_items', through='menu.MenuItemsTags', to='menu.tags'),
        ),
    ]
