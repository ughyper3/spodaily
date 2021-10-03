from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from spodaily_api.models import Exercise, Activity, Routine, Session
from spodaily_api.models_queries import get_activities_by_session, get_sessions_by_routine, get_routine_by_user, get_session_name_by_act_uuid

from spodaily_api.forms import LoginForm, CreateUserForm, EditUserForm, AddSessionForm
from collections import ChainMap

class LoginView(TemplateView):
    template_name = "registration/login.html"

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(email=login_form.cleaned_data.get('email'),
                                password=login_form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Authentification réussie !")
                return HttpResponseRedirect(reverse('home'))

            else:
                messages.error(request,'username or password not correct')

        return HttpResponseRedirect(reverse('login'))


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/home.html"


def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered')
            return HttpResponseRedirect(reverse('login'))

        else:
            messages.error(request, 'Registration failed')

    context = {'form': form}
    return render(request, template_name="registration/register.html", context=context)


def account(request):
    edit_user_form = EditUserForm

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    context = {'edit_user_form': edit_user_form}
    return render(request, template_name="spodaily_api/account.html", context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('dlc_login'))


def routine(request):
    context = {}
    return render(request, 'spodaily_api/routine.html', context)


def session(request):
    context = {}
    user = request.user
    routine = get_routine_by_user(user.uuid)
    session = get_sessions_by_routine(routine.values()[0]['uuid']).values()
    activities_list = []
    for ses in session:
        activity = get_activities_by_session(ses['uuid'])
        activities_list.append(activity)

    context['session'] = session
    context['activity'] = activities_list

    return render(request, 'spodaily_api/session.html', context)

def add_session(request):
    add_session_form = AddSessionForm

    if request.method == 'POST':
        form = AddSessionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    context = {'add_session_form': add_session_form}
    return render(request, 'spodaily_api/add_session.html', context)