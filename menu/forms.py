from django import forms
from .models import Category


class MenuFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__name='Root').exclude(name='Root'),
                                      empty_label="All categories", required=False)
    subcategory = forms.ModelChoiceField(queryset=Category.objects.filter(children=None),
                                         empty_label="All subcategories", required=False)
