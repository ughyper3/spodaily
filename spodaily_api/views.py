from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from spodaily_api.models import Exercise

from spodaily_api.forms import LoginForm, CreateUserForm, UserNameForm, PictureForm


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(email=login_form.cleaned_data.get('email'),
                                password=login_form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        messages.add_message(request, messages.WARNING, "Echec de l'authentification!")
        return HttpResponseRedirect(reverse('login'))


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/home.html"


def routine(request):
    user = request.user

    context = {

    }

    return render(request, 'spodaily_api/routine.html', context)




def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, template_name="spodaily_api/register.html", context=context)


def account(request):
    user_name_form = UserNameForm

    if request.method == 'POST':
        form = UserNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    context = {'user_name_form': user_name_form}
    return render(request, template_name="spodaily_api/account.html", context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('dlc_login'))


