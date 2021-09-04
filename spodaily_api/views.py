from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from spodaily_api.forms import LoginForm, CreateUserForm


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def login(self):
        context = {}
        return render(request=self.request, template_name=self.template_name, context=context)

class LogoutView(TemplateView):
    template_name = "registration/logout.html"

    def logout(self):
        context = {}
        return render(request=self.request, template_name=self.template_name, context=context)


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/home.html"


def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()


    context = {'form': form}
    return render(request, template_name="spodaily_api/register.html", context=context)
