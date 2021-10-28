import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from spodaily_api import views
from spodaily_api.views import DeleteSessionView, DeleteActivityView, AddActivityView, ExerciseGuideView, MuscleView, \
    RoutineView, ContactView, RulesOfUseView, AccountView, PastSessionView, RegisterView, UpdateActivityView

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', RedirectView.as_view(url='spodaily-api/login/', permanent=False)),
    path('spodaily/', include('django.contrib.auth.urls'), name='spodaily_login'),
    url(r'^spodaily/home/', views.Home.as_view(), name='home'),
    url(r'^spodaily/register/', RegisterView.as_view(), name='register'),
    url(r'^spodaily/account/', AccountView.as_view(), name='account'),
    url(r'^spodaily/routine/', RoutineView.as_view(), name='routine'),
    url(r'^spodaily/past_session/', PastSessionView.as_view(), name='past_session'),
    url(r'^spodaily/add_session/', views.AddSessionView.as_view(), name='add_session'),
    url(r'^spodaily/session/', views.SessionView.as_view(), name='session'),
    path('spodaily/delete_session/<uuid:pk>/', DeleteSessionView.as_view(), name='delete_session'),
    path('spodaily/delete_activity/<uuid:pk>/', DeleteActivityView.as_view(), name='delete_activity'),
    path('spodaily/update_activity/<uuid:pk>/', UpdateActivityView.as_view(), name='update_activity'),
    path('spodaily/add_activity/<uuid:fk>/', AddActivityView.as_view(), name='add_activity'),
    url(r'^spodaily/exercise_guide/', ExerciseGuideView.as_view(), name='exercise_guide'),
    path('spodaily/muscle/<uuid:fk>/', MuscleView.as_view(), name='muscle'),
    url(r'^spodaily/contact/', ContactView.as_view(), name='contact'),
    url(r'^spodaily/rule_of_use/', RulesOfUseView.as_view(), name='rules_of_use'),
    path('__debug__/', include(debug_toolbar.urls)),
]
