import uuid

from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.ImageField(upload_to='menu_photos/')
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_text


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    weight_grams = models.IntegerField()
    fat_grams = models.IntegerField()
    carbohydrate_grams = models.IntegerField()
    protein_grams = models.IntegerField()
    is_vegan = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    total_weight_grams = models.IntegerField()
    total_calories = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_prohibited = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    tags = models.ManyToManyField(Tags, through='MenuItemsTags', related_name='menu_items')
    photos = models.ManyToManyField(Photo, related_name='menu_items')
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items')

    @property
    def main_photo(self):
        return self.photos.first()

    def __str__(self):
        return self.name


class MenuItemsTags(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tag', 'menu_item')
