from django import forms
from spodaily_api.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
