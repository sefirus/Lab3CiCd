from django import forms
from .models import Category


class MenuFilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent__name='Root').exclude(name='Root'),
                                              widget=forms.SelectMultiple(attrs={'size': '7'}), required=False)
    subcategory = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(children=None),
                                                 widget=forms.SelectMultiple(attrs={'size': '7'}), required=False)
