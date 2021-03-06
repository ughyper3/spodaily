from django import forms
from django.forms import ModelForm
from spodaily_api.models import Session, Activity, Contact, Exercise, FitnessGoal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'accept_email']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'name', 'birth', 'height', 'weight', 'sexe', 'number_of_session_per_week', 'average_session_length']


class AddSessionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['name', 'date']


class AddActivityForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddActivityForm, self).__init__(*args, **kwargs)
        self.fields['exercise_id'].queryset = Exercise.objects.order_by('name')


    class Meta:
        model = Activity
        fields = ['exercise_id', 'sets', 'repetition', 'rest', 'weight']


class AddContactForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
        fields = ['reason', 'content']


class AddSessionProgramForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSessionProgramForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['name', 'recurrence']


class AddSessionDuplicateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSessionDuplicateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['date']


class SessionDoneForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SessionDoneForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['is_done']


class SettingsProgramSessionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SettingsProgramSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['recurrence', 'name']


class FitnessGoalForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FitnessGoalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FitnessGoal
        fields = ['date', 'exercise', 'weight']