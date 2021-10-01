from django import forms
from django.forms import ModelForm
from spodaily_api.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'user_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserNameForm(ModelForm):
    user_name = forms.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ['user_name']


class PictureForm(ModelForm):
    picture = forms.ImageField(max_length=200)

    class Meta:
        model = User
        fields = ['picture']
