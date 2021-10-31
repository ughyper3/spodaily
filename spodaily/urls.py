from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from spodaily_api import views
from spodaily_api.views import DeleteActivityView, AddFutureActivityView, ExerciseGuideView, \
    MuscleView, \
    RoutineView, RulesOfUseView, AccountView, PastSessionView, RegisterView, UpdateActivityView, Home, \
    RegisterSuccessView, AddContactView, AddPastActivityView, DuplicateProgramSessionView, DeletePastSessionView, \
    DeleteFutureSessionView, DeleteProgramSessionView

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', RedirectView.as_view(url='spodaily/login/', permanent=False)),
    path('spodaily/', include('django.contrib.auth.urls'), name='spodaily_login'),
    url(r'^spodaily/home/', Home.as_view(), name='home'),
    url(r'^spodaily/register/', RegisterView.as_view(), name='register'),
    url(r'^spodaily/register_success/', RegisterSuccessView.as_view(), name='register_success'),
    url(r'^spodaily/account/', AccountView.as_view(), name='account'),
    url(r'^spodaily/routine/', RoutineView.as_view(), name='routine'),
    url(r'^spodaily/past_session/', PastSessionView.as_view(), name='past_session'),
    url(r'^spodaily/add_session/', views.AddFutureSessionView.as_view(), name='add_session'),
    url(r'^spodaily/add_past_session/', views.AddPastSessionView.as_view(), name='add_past_session'),
    url(r'^spodaily/program/', views.ProgramView.as_view(), name='program'),
    url(r'^spodaily/add_program_session/', views.AddProgramSessionView.as_view(), name='add_program_session'),
    path('spodaily/delete_past_session/<uuid:pk>/', DeletePastSessionView.as_view(), name='delete_past_session'),
    path('spodaily/delete_future_session/<uuid:pk>/', DeleteFutureSessionView.as_view(), name='delete_future_session'),
    path('spodaily/delete_program_session/<uuid:pk>/', DeleteProgramSessionView.as_view(), name='delete_program_session'),
    path('spodaily/delete_activity/<uuid:pk>/', DeleteActivityView.as_view(), name='delete_activity'),
    path('spodaily/update_activity/<uuid:pk>/', UpdateActivityView.as_view(), name='update_activity'),
    path('spodaily/add_activity/<uuid:fk>/', AddFutureActivityView.as_view(), name='add_activity'),
    path('spodaily/duplicate_program_session/<uuid:fk>/', DuplicateProgramSessionView.as_view(), name='duplicate_program_session'),
    path('spodaily/add_past_activity/<uuid:fk>/', AddPastActivityView.as_view(), name='add_past_activity'),
    url(r'^spodaily/exercise_guide/', ExerciseGuideView.as_view(), name='exercise_guide'),
    path('spodaily/muscle/<uuid:fk>/', MuscleView.as_view(), name='muscle'),
    url(r'^spodaily/contact/', AddContactView.as_view(), name='contact'),
    url(r'^spodaily/rule_of_use/', RulesOfUseView.as_view(), name='rules_of_use'),
]
