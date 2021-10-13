from django import forms
from django.forms import ModelForm
from spodaily_api.models import User, Session, Activity
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
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(ModelForm):
    email = forms.EmailField(required=True, max_length=150)
    first_name = forms.CharField(required=False, max_length=150)
    name = forms.CharField(required=False, max_length=150)
    birth = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'name', 'birth']


class AddSessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'date']

    def __init__(self, *args, **kwargs):
        super(AddSessionForm, self).__init__(*args, **kwargs)


class AddActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['session_id', 'exercise_id', 'sets', 'repetition', 'rest', 'weight']