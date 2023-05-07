from django import forms
from .models import Category, Tags


class MenuFilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent__name='Root').exclude(name='Root'),
                                              widget=forms.SelectMultiple(attrs={'size': '7'}), required=False)
    subcategory = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(children=None),
                                                 widget=forms.SelectMultiple(attrs={'size': '7'}), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.SelectMultiple(attrs={'size': '5'}),
                                          required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
