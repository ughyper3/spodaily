from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from spodaily_api import views


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', RedirectView.as_view(url='spodaily-api/login/', permanent=False)),
    path('spodaily-api/', include('django.contrib.auth.urls'), name='spodaily_login'),
    url(r'^spodaily-api/home/', views.Home.as_view(), name='home'),
    url(r'^spodaily-api/register/', views.register, name='register'),
    url(r'^spodaily-api/account/', views.account, name='account'),
    url(r'^spodaily-api/routine/', views.routine, name='routine'),
    url(r'^spodaily-api/session/', views.session, name='session'),
    url(r'^spodaily-api/add_session/', views.add_session, name='add_session'),


]
