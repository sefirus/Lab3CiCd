# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class WaiterLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
