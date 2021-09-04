from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from spodaily_api.forms import LoginForm


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def login(self):
        context = {}
        return render(request=self.request, template_name=self.template_name, context=context)


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/home.html"


class Register(TemplateView):
    template_name = "spodaily_api/register.html"

